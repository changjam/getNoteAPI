FROM python:3.11-slim-buster

WORKDIR /app

COPY .env .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src .

EXPOSE 8000

CMD python api.py