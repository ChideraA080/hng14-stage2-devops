# Stage 1: builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Install dependencies normally (FIXED)
ENV PIP_DEFAULT_TIMEOUT=300
ENV PIP_RETRIES=20

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install \
    --no-cache-dir \
    --prefer-binary \
    --timeout 300 \
    --retries 20 \
    -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim

WORKDIR /app

# Minimal OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

# Copy installed packages properly
COPY --from=builder /usr/local /usr/local

# Copy app source
COPY . .

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/app

USER appuser

# Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://api:8000/health || exit 1

CMD ["python", "worker.py"]
