from app.celery_app import celery_app
import time

@celery_app.task
def test_task(name: str):
    """Test task to verify Celery is working"""
    time.sleep(5) # Simulate some work
    return f"Hello {name}, task completed."

@celery_app.task
def add_numbers(x: int, y: int):
    """Test task"""
    return x + y