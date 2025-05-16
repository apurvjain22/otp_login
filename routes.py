import datetime

import redis
from fastapi import FastAPI, APIRouter, Request, HTTPException, status
from schema import LoginRequest, VerifyRequest
from slowapi.util import get_remote_address, get_ipaddr
from slowapi import Limiter

from util import verify_user_limit, generate_otp
from tasks import send_otp_via_sms
from redis_client import r

app = FastAPI()
router = APIRouter(tags=['OTP Routes'])

# slow rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter


@router.post('/login')
@limiter.limit("20/minute")  # endpoint limit per min
# @limiter.limit("1/minute", key_func=get_remote_address)  # on IP
@limiter.limit("1/minute", key_func=verify_user_limit)  # user mobile
async def otp_login(req: LoginRequest, request: Request):
    """ it will basically generate otp and save it to redis """
    print("otp login...")
    ip = get_ipaddr(request)
    print(f"Incoming request from IP: {ip}")
    mobile = req.mobile
    print(f"mobile: {mobile}")
    if not len(mobile) == 10:  # validating mobile number
        return HTTPException(detail="Not a valid mobile number",
                             status_code=status.HTTP_400_BAD_REQUEST)
    # generate 4 digit otp
    otp = generate_otp()
    # preparing data for redis
    try:
        a = r.set(f"otp: {mobile}", f"{otp}", ex=60)  # return bool
    except redis.exceptions.RedisError as e:
        print("Redis error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    print(f"return value after saving in redis: {a}")
    # rate window key like
    rate_key = "otp:rate:" + datetime.datetime.utcnow().strftime("%Y%m%d%H%M")
    current_count = r.incr(rate_key)
    if current_count == 1:
        r.expire(rate_key, 60)
    if current_count <= 10:
        send_otp_via_sms.delay(mobile, otp)  # this will immediately execute
        # the task
        return {"status": "OTP sent immediately"}
    else:
        send_otp_via_sms.apply_async((mobile, otp), countdown=60) # this
        # will delay the task and run it after 60 seconds
        return {
            "status": "Rate exceeded — OTP is queued and will be sent shortly"
        }


@router.post('/verify_otp')
async def verify(data: VerifyRequest):
    """ verifying the otp received from the user's mobile """
    print("verifying users otp...")
    user_otp = data.user_otp
    mobile = data.mobile
    saved_otp = r.get(f'otp: {mobile}')
    if saved_otp == user_otp:
        print("otp is verified")
        return "Verified"
