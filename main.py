from fastapi import FastAPI

import sqlalchemy.orm as orm
import sqlalchemy as sqla

class Base(orm.DeclarativeBase):
    pass

class Question(Base):
    __tablename__ = "questions"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    text: orm.Mapped[str] = orm.mapped_column(sqla.String(256))
    answer: orm.Mapped[str] = orm.mapped_column(sqla.String(64))

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello, ": "World!"}

