import os
import time

from celery import Celery
from celery.schedules import crontab
from celery.result import AsyncResult

from models import ModelTask

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.broker_url = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kw):
    sender.add_periodic_task(2.5, modify_db_tasks.s(), name='Modify db tasks')

@celery.task(name='sleep')
def sleep(task_length):
    time.sleep(int(task_length))
    return 'Slept long enough'


@celery.task(name='')
def modify_db_tasks(*_):
    print('*** Modifying db tasks ***')
    bad_task_statuses = ['PENDING', 'STARTED', 'RETRY']
    
    for bad_status in bad_task_statuses:
        db_tasks = ModelTask.get_by_status(bad_status)
        for db_task in db_tasks:
            task_result = AsyncResult(db_task)
            db_task.change_to(task_result)
