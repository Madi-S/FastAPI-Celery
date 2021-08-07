from typing import Any, Optional
from pydantic import BaseModel


class SchemaUser(BaseModel):
    first_name: str
    last_name: str = None
    age: int

    class Config:
        orm_mode = True


class SchemaTask(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    result: Optional[str] = None
    additional_data: Optional[str] = None

    class Config:
        orm_mode = True
