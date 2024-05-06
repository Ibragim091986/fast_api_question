from typing import List
from question_app.api.db import questions, database
from question_app.api.models import QuestionNew


async def added_questions(question_models: List[QuestionNew]):
    values = [item.dict() for item in question_models]
    query = questions.insert().values(values)
    return await database.execute(query=query)


async def find_question_by_text(text: str):
    query = questions.select().where(questions.c.text == text)
    return await database.fetch_one(query=query)


async def find_last_request_question():
    query = questions.select().order_by(questions.c.created_at.desc()).limit(1)
    last_record = await database.fetch_one(query=query)
    if last_record:
        request_uuid = last_record['request_uuid']
        query_all = questions.select().where(questions.c.request_uuid == request_uuid)
        all_records = await database.fetch_all(query=query_all)
        return all_records
    else:
        return []
