FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

CMD redis-server --daemonize yes && python3 app.py
