from typing import Union
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

global todo_list, last_todo_id
todo_list = {}
last_todo_id = 0


class ToDo(BaseModel):
    todo_id: int
    content: str
    is_done: bool = False


# listup todos
@app.get("/todos")
def list_todo():
    return {"todos": todo_list}


# get todo from id
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    return todo_list[todo_id]


# post todo
@app.post("/todo")
def post_todo(content: str):
    global last_todo_id
    todo_id = last_todo_id
    last_todo_id += 1
    new_todo = ToDo(
        todo_id=todo_id,
        content=content,
    )
    todo_list[todo_id] = new_todo
    return todo_list[todo_id]


# delete todo
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    del todo_list[todo_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)