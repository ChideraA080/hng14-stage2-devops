# Stage 1: build dependencies
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

ENV PIP_DEFAULT_TIMEOUT=120

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --timeout=120 --retries=10 --target=/install -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# security patching (IMPORTANT for Trivy)
RUN apt-get update && apt-get upgrade -y && apt-get clean

# create non-root user
RUN useradd -m appuser

# copy dependencies
COPY --from=builder /install /install

# copy app code
COPY . .

ENV PATH=/install/bin:$PATH
ENV PYTHONPATH=/install

USER appuser

# healthcheck (worker has no HTTP server)
HEALTHCHECK CMD python -c "import os, redis; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379))); r.ping()" || exit 1

CMD ["python", "worker.py"]
