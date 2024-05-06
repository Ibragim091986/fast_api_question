import asyncio
import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from question_app.api.db_manager import added_questions, find_question_by_text, find_last_request_question
from question_app.api.models import QuestionNew, QuestionIn
from question_app.services import opentdb_service

survey = APIRouter()


@survey.post('/', status_code=201)
async def question(payload: QuestionIn):
    if payload.questions_num < 1:
        raise HTTPException(status_code=400, detail="Недопустимое количество вопросов.")
    last_request = await find_last_request_question()

    async def process_questions():
        try:
            questions = await opentdb_service.get_questions(payload, 0.2)
            common_uuid = uuid4()
            question_models = []
            for item in questions:
                # Проверяем наличие вопроса в базе данных и в списке
                existing_question = await find_question_by_text(item['question'])
                # Если вопрос найден, запросить новый вопрос
                while existing_question:
                    new_questions = await opentdb_service.get_questions(QuestionIn(questions_num=1), 0.2)
                    if not new_questions:
                        logging.error(f"Не удалось получить новые вопросы.: {new_questions}")
                        raise HTTPException(status_code=503, detail="Не удалось получить новые вопросы.")
                    item = new_questions[0]
                    existing_question = await find_question_by_text(item['question'])

                question_model = QuestionNew(
                    text=item['question'],
                    correct_answer=item['correct_answer'],
                    request_uuid=common_uuid
                )
                question_models.append(question_model)

            await added_questions(question_models)
        except HTTPException as e:
            logging.error(f"Ошибка в ассихронном методе: {e.detail}")
            raise HTTPException(status_code=503, detail="Ошибка в ассихронном методе.")

    asyncio.create_task(process_questions())

    return last_request
