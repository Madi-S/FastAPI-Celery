import os
import time

from celery import Celery

<<<<<<< HEAD
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.broker_url = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

@celery.task(name='create_task')
def create_task(task_length):
    time.sleep(int(task_length) * 3)
=======

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
>>>>>>> 2ecc122a28b50dc08ab318486c6de0c7c95757db
    return True
