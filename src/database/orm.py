from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index = True)
    contents = Column(String(256), nullable = False)
    is_done = Column(Boolean, default = False)

    def __repr__(self):
        return f"Todo(id={self.id}, contents={self.contents}, is_done={self.is_done})"