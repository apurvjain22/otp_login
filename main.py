from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from routes import router
from util import custom_rate_limit_exception

app = FastAPI(title='OTP Login')

app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exception)

app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8001)
