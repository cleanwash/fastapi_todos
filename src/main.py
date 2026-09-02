from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

todo_datas = {
    1: {
        "id" :1,
        "contents":"실전! FastAPI 섹션 0 수강",
        "is_done" : True,
    },
    2: {
        "id" :2,
        "contents":"실전! FastAPI 섹션 1 수강",
        "is_done" : False,
    },
    3: {
        "id" :3,
        "contents":"실전! FastAPI 섹션 2 수강",
        "is_done" : False,
    }
}

@app.get("/todos")
def get_todos(order:str | None = None ):
    ret = list(todo_datas.values())
    if order and order == 'DESC':
        return ret[::-1]
    return ret

@app.get("/todos/{todo_id}")
def get_todo_handler(todo_id:int):
    return todo_datas.get(todo_id, {})

class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

@app.post("/todos")
def create_todo_handler(request: CreateTodoRequest):
    todo_datas[request.id] = request.dict()
    return todo_datas[request.id]

@app.patch("/todos/{todo_id}")
def update_todo_handler(
        todo_id:int,
        is_done :bool = Body(..., embed=True),
):
    todo = todo_datas.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    return {}