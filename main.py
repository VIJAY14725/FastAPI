from fastapi import FastAPI, HTTPException
from typing import List
from models import Create, Update, User
from dependencies import get_current_user
from sqlalchemy import Column, Integer, String
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from database import engine, Base, sessionLocal
from sqlalchemy.orm import Session
from schemas import Todo, Create, Update

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI OAUTH2 JWT", version="1.0.0")

todos_db: dict[int, Todo] = {}


app = FastAPI(title="Todo API", version="1.0.0")


@app.get("/task", response_model=List[Todo], tags=["Task"])
def get_todos():
    return list(todos_db.values())


@app.get("/task/{task_id}", response_model=Todo, tags=["Task"])
def get_todo(task_id: int):
    if task_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[task_id]


@app.post("/task", response_model=Todo, status_code=201, tags=["Task"])
def create_todo(todo: Create):
    todo_id = max(todos_db.keys(), default=0) + 1
    new_todo = Todo(id=todo_id, **todo.dict())
    todos_db[todo_id] = new_todo
    return new_todo


@app.put("/task/{task_id}", response_model=Todo, tags=["Task"])
def update_todo(task_id: int, todo: Update):
    if task_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo = todos_db[task_id].copy(
        update=todo.dict(exclude_unset=True)
    )
    todos_db[task_id] = updated_todo
    return updated_todo


@app.delete("/task/{task_id}", status_code=204, tags=["Task"])
def delete_todo(task_id: int):
    if task_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[task_id]
    return
