from typing import Union
from fastapi import FastAPI, HTTPException, Response, status, Body
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 이미 생성된 FastAPI app 인스턴스에 CORS 미들웨어를 추가합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처를 허용하거나 특정 출처 리스트를 명시할 수 있습니다.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드를 허용하거나 ['GET', 'POST', ...] 같이 명시할 수 있습니다.
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용하거나 ['Content-Type', ...] 같이 명시할 수 있습니다.
)

todo_list = {}
last_todo_id = 0

# 할 일 항목을 정의하는 모델
class ToDoBase(BaseModel):  # 클라이언트가 제공하는 필드만 포함
    content: str = Field(..., min_length=1, max_length=200)
    is_done: bool = Field(default= False)

class ToDo(ToDoBase):  # 서버에서 관리하는 todo_id를 추가
    todo_id: int

# 모든 할 일 항목을 나열
@app.get("/todos")
def list_todo():
    return {"todos": list(todo_list.values())}

# 특정 ID의 할 일 항목을 가져옴
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = todo_list.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

# 새 할 일 항목을 생성
@app.post("/todos", response_model=ToDo)
def post_todo(todo: ToDoBase):  # ToDoBase를 사용하여 요청 데이터를 받음
    global last_todo_id
    todo_id = last_todo_id
    last_todo_id += 1
    todo_dict = todo.dict()
    todo_dict.update({"todo_id": todo_id})
    todo_list[todo_id] = todo_dict
    return todo_dict

# 특정 ID의 할 일 항목을 삭제
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    if todo_id not in todo_list:
        raise HTTPException(status_code=404, detail="ToDo not found")
    del todo_list[todo_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
