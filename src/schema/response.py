from typing import List

from pydantic import BaseModel, ConfigDict

class ToDoSchema(BaseModel):
    id:int
    contents:str
    is_done:bool

    # pydantic v2 문법: orm_mode(v1) -> from_attributes(v2)
    # SQLAlchemy 객체(속성 접근)를 그대로 읽어서 검증/변환할 수 있게 해줌
    model_config = ConfigDict(from_attributes=True)

class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema]