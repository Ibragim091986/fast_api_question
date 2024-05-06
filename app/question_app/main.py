import logging

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from question_app.api.db import database
from question_app.api.survey import survey


app = FastAPI()
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)



@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()


app.include_router(survey, prefix='/api/v1/question')
