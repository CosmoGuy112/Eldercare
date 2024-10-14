FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000