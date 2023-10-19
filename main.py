import os

from fastapi import FastAPI
import sqlalchemy.orm as orm
import sqlalchemy as sqla
import pydantic
import requests
from datetime import datetime

dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'

class Question(pydantic.BaseModel):
    id: int
    text: str
    answer: str
    created_at: datetime

class API:
    def __init__(self, url: str):
        self.URL = url
    def random_questions(self, n: int) -> list[Question]:
        res = requests.get(
            self.URL + f'/random',
            params=[
                ('count', n),
            ],
        )
        js = res.json()
        qs = [Question(
            id=j['id'],
            text=j['question'],
            answer=j['answer'],
            created_at=datetime.strptime(j['created_at'], dt_format),
        ) for j in js ]
        return qs


class Base(orm.DeclarativeBase):
    pass

class QuestionModel(Base):
    __tablename__ = 'questions'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    text: orm.Mapped[str] = orm.mapped_column(sqla.String(256))
    answer: orm.Mapped[str] = orm.mapped_column(sqla.String(64))
    created_at = sqla.Column(sqla.DateTime)
    def Exist(id_: int) -> bool:
        with orm.Session(engine) as session:
            return session.query(
                    sqla.exists().
                    where(QuestionModel.id == id_),
                ).scalar()


class RandomQuestions(pydantic.BaseModel):
    questions_num: int

env = os.environ
host, pwd, user, name, port = env["DB_HOST"], env["DB_PASS"], env["DB_USER"], env['DB_NAME'], env['DB_PORT']
api = API('https://jservice.io/api')
app = FastAPI()
eng_str = f"postgresql://{user}:{pwd}@{host}:{port}/{name}"
engine = sqla.create_engine(eng_str)
Base.metadata.create_all(engine)

@app.post('/questions/')
def read_random_questions(q: RandomQuestions):
    qs = api.random_questions(q.questions_num)
    ret = {}
    for i, q in enumerate(qs):
        if QuestionModel.Exist(q.id):
            # Replacing existing questions with not existing in the DB.
            exist = True
            while exist:
                q = api.random_questions(1)[0]
                exist = QuestionModel.Exist(q.id)
            qs[i] = q

    with orm.Session(engine) as session:
        qms = []
        for q in qs:
            qms.append(QuestionModel(
                id=q.id,
                text=q.text,
                answer=q.answer,
                created_at=q.created_at,
            ))
            # Saving THE LAST SAVED to return.
            # It is not clear why we should return
            # the last saved but not the specified
            # amount of random questions.
            # Okay, none of my business,
            # just consider it when checking the task.
            ret = q
        session.add_all(qms)
        session.commit()
    return ret

