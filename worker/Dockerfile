# Stage 1: build dependencies
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

ENV PIP_DEFAULT_TIMEOUT=300
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

RUN pip install --upgrade pip setuptools wheel && \
    pip install \
    --no-cache-dir \
    --default-timeout=300 \
    --timeout=300 \
    --retries 50 \
    --target=/install \
    -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# security patching (IMPORTANT for Trivy)
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

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
