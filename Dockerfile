FROM tiangolo/uvicorn-gunicorn:python3.11-slim

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY app/requirements.txt /tmp/requirements.txt
COPY ./.env /app/.env
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "question_app.main:app"]
