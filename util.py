from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from redis_client import r
import random


async def custom_rate_limit_exception(request: Request,
                                      exc: RateLimitExceeded):
    try:
        body = await request.json()
        mobile = body.get("mobile")
        existing_otp = r.get(f"otp: {mobile}")
        print("existing_otp", existing_otp)
        if existing_otp:
            return JSONResponse(
                status_code=429,
                content={
                    "message": "OTP already sent and is still valid.",
                    "otp": existing_otp
                }
            )
    except Exception:
        pass  # fallback
    # Fallback in all other cases (including IP-based rate limits)
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Please try again later."}
    )


def verify_user_limit(request: Request) -> str:
    try:
        value = request.headers.get("X-User-Mobile", "")
        print(f"data: {value}")
        return value
    except Exception:
        return "Error while verifying user limit"


def generate_otp():
    return str(random.randint(1000, 9999))  # 4-digit OTP
