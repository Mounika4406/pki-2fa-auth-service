FROM python:3.11-slim

WORKDIR /app
ENV TZ=UTC

RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=120 -r requirements.txt


COPY app app
COPY scripts scripts

COPY student_private.pem student_private.pem

COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron
RUN mkdir -p /data /cron



EXPOSE 8080

CMD ["sh", "-c", "cron -f & python -m uvicorn app.main:app --host 0.0.0.0 --port 8080"]
