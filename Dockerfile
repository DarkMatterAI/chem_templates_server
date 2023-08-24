FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN chmod +x /code/app/tests/tests-start.sh

ENV PORT=7860
ENV HOST=0.0.0.0
ENV WORKERS=1
ENV TIMEOUT=120
ENV MONGO_URI=
ENV MONGO_DB_NAME=template_db

CMD uvicorn app.main:app --host $HOST --port $PORT --workers $WORKERS --timeout-keep-alive $TIMEOUT
