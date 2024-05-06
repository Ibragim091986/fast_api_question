import asyncio
import logging

import httpx
from fastapi import HTTPException
from question_app.api.models import QuestionIn


async def get_questions(payload: QuestionIn, delay: float = None):
    try:
        if delay:
            await asyncio.sleep(delay)
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://opentdb.com/api.php?amount={payload.questions_num}')
            if response.status_code != 200:
                logging.error(f"Ошибка при запросе к внешнему API: ODE: {response.status_code}")
                raise HTTPException(status_code=response.status_code, detail="Ошибка при запросе к внешнему API")

            return response.json().get('results', [])
    except Exception as e:
        logging.error(f"Общая ошибка при запросе к внешнему API.")
        raise HTTPException(status_code=500, detail=str(e))
