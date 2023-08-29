FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN chmod +x /code/app/tests/tests-start.sh

ENV TEMPLATE_SERVER_PORT=7860
ENV TEMPLATE_SERVER_HOST=0.0.0.0
ENV TEMPLATE_SERVER_WORKERS=1
ENV TEMPLATE_SERVER_TIMEOUT=120
ENV MONGO_URI=
ENV MONGO_DB_NAME=template_db

CMD uvicorn app.main:app --host $TEMPLATE_SERVER_HOST --port $TEMPLATE_SERVER_PORT --workers $TEMPLATE_SERVER_WORKERS --timeout-keep-alive $TEMPLATE_SERVER_TIMEOUT
