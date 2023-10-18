from fastapi import FastAPI

import sqlalchemy.orm as orm
import sqlalchemy as sqla
import pydantic
import requests

class API:
    def __init__(self, url: str):
        self.URL = url
    def Random(self, n: int):
        res = requests.get(
            self.URL + f'/random',
            params=[
                ('count', n),
            ],
        )
        return res


class Base(orm.DeclarativeBase):
    pass

class QuestionTable(Base):
    __tablename__ = 'questions'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    text: orm.Mapped[str] = orm.mapped_column(sqla.String(256))
    answer: orm.Mapped[str] = orm.mapped_column(sqla.String(64))

class RandomQuestions(pydantic.BaseModel):
    questions_num: int

api = API('https://jservice.io/api')
app = FastAPI()

@app.post('/questions/')
def read_random_questions(q: RandomQuestions):
    res = api.Random(q.questions_num)
    return res.content

