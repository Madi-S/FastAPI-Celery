from typing import Any, List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from fastapi_sqlalchemy import db


Base = declarative_base()


class CreateMixin:

    @classmethod
    def create(cls, **data) -> Any:
        obj = cls(**data)
        db.session.add(obj)
        db.session.commit()
        return obj


class ModelUser(Base, CreateMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)


class ModelTask(Base, CreateMixin):
    __tablename__ = 'task'
    id = Column(String, primary_key=True)
    status = Column(String, default='PENDING')
    result = Column(String)
    additional_data = Column(String)

    def change_to(self, task_result: Any) -> None:
        self.set_status(task_result.status)
        self.set_result(task_result.result)

    def set_result(self, result: str) -> None:
        self.result = result
        db.session.commit()

    def set_status(self, status: str) -> None:
        self.status = status
        db.session.commit()
        
    def set_additional_data(self, data: str) -> None:
        self.additional_data = 'Changed via celery'
        
    @classmethod
    def get_by_id(cls, id: str) -> Any:
        return db.session.query(cls).get(id)

    @classmethod
    def get_from_to(cls, start: int, end: int) -> List[Any]:
        return db.session.query(cls).offset(start).limit(end - start).all()

    @classmethod
    def get_by_status(cls, status: str) -> List[Any]:
        return db.session.query(cls).filter_by(status=status).all()
