# fastapi 패키지에서 FastAPI 클래스, Body(요청 body 값을 세부 제어하는 도구)를 가져옴
from fastapi import FastAPI, Body, HTTPException
# pydantic 패키지에서 BaseModel(요청/응답 데이터 검증용 클래스)을 가져옴
from pydantic import BaseModel
from starlette import status

# FastAPI 클래스를 인스턴스화(실제 실행 가능한 객체로 생성) -> 이 app이 서버의 진입점
app = FastAPI()

# GET / -> 서버가 살아있는지 확인하는 헬스체크용 엔드포인트
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}

# 임시 DB 역할을 하는 딕셔너리
# key(1, 2, 3)가 실제 조회/수정 시 사용되는 id -> 값 안의 "id" 필드와는 별개의 존재
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

# GET /todos?order=DESC
# order: 함수에만 있고 경로({})에는 없으므로 query parameter -> 기본값(None)이 있어 선택값
@app.get("/todos", status_code=200)
def get_todos(order:str | None = None ):
    ret = list(todo_datas.values())
    if order and order == 'DESC':
        return ret[::-1]  # 역순 정렬
    return ret

# GET /todos/{todo_id}
# todo_id: 경로의 {todo_id}와 이름이 일치하므로 path parameter -> 기본값 없어 필수
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id:int):
    todo = todo_datas.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail='ToDo Not Found')


# POST body 검증용 스키마 (pydantic 모델)
# 클라이언트가 보낸 JSON을 이 필드들에 맞춰 자동 검증/변환해줌
class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

# POST /todos
# request: CreateTodoRequest -> FastAPI가 요청 body(JSON)를 자동으로 이 타입 객체로 변환해서 넘겨줌
@app.post("/todos", status_code = 201)
def create_todo_handler(request: CreateTodoRequest):
    # request.dict(): pydantic 객체 -> 순수 딕셔너리로 변환
    # todo_datas[request.id]: request.id 값을 "키"로 사용해 새 항목 추가(이미 있으면 덮어씀)
    todo_datas[request.id] = request.dict()
    return todo_datas[request.id]

# PATCH /todos/{todo_id}
# todo_id: path parameter (필수)
# is_done: Body(..., embed=True)
#   - "...": 기본값 없음 -> 필수값이라는 뜻 (값 자체를 제한하는 게 아님, true/false 둘 다 허용)
#   - embed=True: body를 {"is_done": true} 처럼 필드명으로 감싼 형태로 받겠다는 뜻
#     (embed=False였다면 body가 true/false 값 하나만 오는 형태를 기대함)
@app.patch("/todos/{todo_id}")
def update_todo_handler(
        todo_id:int,
        is_done :bool = Body(..., embed=True),
):
    todo = todo_datas.get(todo_id)  # 해당 id의 todo "딕셔너리 자체"를 가져옴 (없으면 None)
    if todo:
        # todo는 todo_datas 안의 원본과 같은 객체를 가리키므로,
        # 여기서 값을 바꾸면 todo_datas 원본도 함께 바뀜 (별도 재대입 불필요)
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")
    return {}


# DELETE /todos/{todo_id}
# todo_id: path parameter (필수)
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id:int):
    # .pop(key, default): key에 해당하는 항목을 삭제하면서 그 값을 반환
    # key가 없어도 default(None) 덕분에 에러 없이 그냥 넘어감 (없는 id를 지워도 안전)
    todo = todo_datas.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="ToDo Not Found")
    # return todo_datas  # 삭제 후 남은 전체 todo 목록을 응답으로 반환