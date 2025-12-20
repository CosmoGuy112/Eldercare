FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client iputils-ping && apt-get clean

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]