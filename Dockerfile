FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV HOST 0.0.0.0

ENV PORT 8000

CMD uvicorn main:app --reload --host $HOST --port $PORT