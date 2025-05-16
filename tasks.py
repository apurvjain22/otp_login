from celery import Celery

celery = Celery(
    "otp_tasks",
    broker="redis://localhost:6379/0",  # where tasks are sent
    backend="redis://localhost:6379/0"  # where celery stores task results
)
# This config sets routing rules
# It says: tasks with the name "tasks.send_otp_via_sms" should go to the Redis queue named otp_queue.
celery.conf.task_routes = {
    "tasks.send_otp_via_sms": {"queue": "otp_queue"},
}


# This fn is marked as Celery task
@celery.task
def send_otp_via_sms(mobile: str, otp: str):
    print(f"sending {otp} to mobile number {mobile}")
