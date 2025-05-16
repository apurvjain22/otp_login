# OTP Sending Service using FastAPI, Celery, and Redis

This is a simple backend service that sends OTPs (One-Time Passwords) to users via SMS. It uses:

- **FastAPI** for the API layer
- **Celery** for asynchronous task processing
- **Redis** as a message broker and rate limiter

## Features

- Send OTP to a given mobile number
- Rate limiting: only 10 OTPs can be sent per minute
- Queued OTP delivery: if rate limit is exceeded, OTPs are delayed using Celery
- Asynchronous processing using Celery with Redis
- Environment-independent (works locally and can scale with Docker or cloud services)

---

## 🛠️ Tech Stack

- **FastAPI**: Backend framework
- **Celery**: Task queue manager
- **Redis**: Message broker and result backend (via Docker)
- **Python**: Language
- **Docker**: For running Redis

---

## Installation

### 1. Clone the repository

git clone https://github.com/your-username/otp-service.git 

cd otp-service


### To start the redis server
docker run --name redis-server -p 6379:6379 -d redis

