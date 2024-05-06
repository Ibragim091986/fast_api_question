from uuid import UUID
from pydantic import BaseModel


class QuestionIn(BaseModel):
    questions_num: int


class QuestionNew(BaseModel):
    text: str
    correct_answer: str
    request_uuid: UUID
