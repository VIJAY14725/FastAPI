from fastapi import FastAPI, HTTPException
from typing import List
from models import Todo, TodoCreate, TodoUpdate
from database import todos_db

app = FastAPI(title="Todo API", version="1.0.0")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI Todo API"}


@app.get("/todos", response_model=List[Todo], tags=["Todos"])
def get_todos():
    return list(todos_db.values())


@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def get_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos_db[todo_id]


@app.post("/todos", response_model=Todo, status_code=201, tags=["Todos"])
def create_todo(todo: TodoCreate):
    todo_id = max(todos_db.keys(), default=0) + 1
    new_todo = Todo(id=todo_id, **todo.dict())
    todos_db[todo_id] = new_todo
    return new_todo


@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def update_todo(todo_id: int, todo: TodoUpdate):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo = todos_db[todo_id].copy(update=todo.dict(exclude_unset=True))
    todos_db[todo_id] = updated_todo
    return updated_todo


@app.delete("/todos/{todo_id}", status_code=204, tags=["Todos"])
def delete_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos_db[todo_id]
    return None
