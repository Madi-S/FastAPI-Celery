import os
from typing import Any, List
from dotenv import load_dotenv

from fastapi import Body, FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_sqlalchemy import DBSessionMiddleware

from worker import sleep
from models import ModelUser, ModelTask
from schema import SchemaUser, SchemaTask


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware,
    db_url=os.environ['DATABASE_URL']
)

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request})


@app.get('/tasks', response_model=List[SchemaTask], tags=['tasks'])
def get_tasks(start: int = 0, end: int = 10):
    if end <= start:
        raise HTTPException(418, 'End must greater than start')

    db_tasks = ModelTask.get_from_to(start, end)
    return db_tasks


@app.get('/tasks/{task_id}', response_model=SchemaTask, tags=['tasks'])
def get_task_by_id(task_id):
    db_task = ModelTask.get_by_id(task_id)
    return db_task


@app.post('/tasks', response_model=SchemaTask, status_code=201, tags=['tasks'])
def post_tasks(payload=Body(...)):
    task = fire_sleep_task(payload)
    db_task = ModelTask.create(id=task.id)
    return db_task


def fire_sleep_task(payload: dict):
    task_delay = payload['delay']
    task = sleep.delay(int(task_delay))
    return task


@app.post('/users/', response_model=SchemaUser, tags=['users'])
def post_users(user: SchemaUser):
    db_user = ModelUser.create(**user.dict())
    return db_user

@app.get('/test/')
def test():
    return {'hello': 'world'}
