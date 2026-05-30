# Stage 1: builder
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

# Install dependencies normally (IMPORTANT FIX)
ENV PIP_DEFAULT_TIMEOUT=300
ENV PIP_RETRIES=20

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install \
    --no-cache-dir \
    --prefer-binary \
    --disable-pip-version-check \
    --timeout 300 \
    --retries 20 \
    -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install minimal OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gcc && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy app source
COPY . .

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://localhost:8000/health || exit 1

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
