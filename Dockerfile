FROM python:3.11-slim

WORKDIR /app
ENV TZ=UTC

RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY scripts scripts
COPY cron/2fa-cron /tmp/2fa-cron
COPY student_private.pem student_private.pem

RUN chmod 644 /tmp/2fa-cron && crontab /tmp/2fa-cron
RUN mkdir -p /data /cron

EXPOSE 8080

CMD sh -c "cron && python -m uvicorn app.main:app --host 0.0.0.0 --port 8080"
