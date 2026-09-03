from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.orm import Todo


def get_todos(session:Session)-> List[Todo]:
    return list(session.scalars(select(Todo)))


def get_todo_by_todo_id(session:Session, todo_id:int) -> Todo | None:
    return session.scalars(select(Todo).where(Todo.id == todo_id)).first()