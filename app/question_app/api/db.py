import os

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, DateTime, func)
from databases import Database

DATABASE_URL = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

questions = Table(
    'questions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String),  # текст вопроса
    Column('correct_answer', String),  # правильный ответ
    Column('request_uuid', String),  # UUID запроса для группировки вопросов
    Column('created_at', DateTime, default=func.now())  # время создания записи
)

database = Database(DATABASE_URL)
