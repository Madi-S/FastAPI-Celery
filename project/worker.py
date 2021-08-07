import os
import time
import requests

from celery import Celery
from celery.schedules import crontab
from celery.result import AsyncResult

from models import ModelTask

celery = Celery('proj')
celery.conf.broker_url = os.environ.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.broker_url = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kw):
#     sender.add_periodic_task(2.5, modify_db_tasks.s('Hello'), name='Modify db tasks')
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

@celery.task
def test_task(arg):
    requests.post('http://localhost:8004/users', json={
        'first_name': 'Madi',
        'last_name': 'Madi',
        'age': 50
    })


@celery.task
def add(x, y):
    z = x + y
    requests.post('http://localhost:8004/users', json={
        'first_name': 'Madi',
        'last_name': 'Madi',
        'age': 50
    })


@celery.task(name='sleep')
def sleep(task_length):
    requests.post('http://localhost:8004/users', json={
        'first_name': 'Madi',
        'last_name': 'Madi',
        'age': 50
    })
    time.sleep(int(task_length))
    return True


@celery.task(name='')
def modify_db_tasks(*_):
    print('*** Modifying db tasks ***')
    bad_task_statuses = ['PENDING', 'STARTED', 'RETRY']
    
    for bad_status in bad_task_statuses:
        db_tasks = ModelTask.get_by_status(bad_status)
        for db_task in db_tasks:
            task_result = AsyncResult(db_task)
            db_task.change_to(task_result)
