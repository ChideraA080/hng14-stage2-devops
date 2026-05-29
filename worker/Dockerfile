FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install \
    --no-cache-dir \
    --default-timeout=600 \
    --retries 20 \
    --timeout 600 \
    --prefer-binary \
    --target=/install \
    -r requirements.txt

FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

COPY --from=builder /install /install
COPY . .

ENV PATH=/install/bin:$PATH
ENV PYTHONPATH=/install

USER appuser

HEALTHCHECK CMD python -c "import os, redis; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379))); r.ping()" || exit 1

CMD ["python", "worker.py"]
