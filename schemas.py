from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

class Create(BaseModel):
    title: str
    completed: bool = False

class Update(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
