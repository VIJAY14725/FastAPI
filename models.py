from pydantic import BaseModel, Field
from typing import Optional

class Base(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    completed: bool = False

class Create(Base):
    pass

class Update(Base):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    completed: Optional[bool] = None

class Todo(Base):
    id: int
