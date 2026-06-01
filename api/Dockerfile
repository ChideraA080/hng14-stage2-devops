# Builder stage
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# ONLY essential security update
RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd -m appuser

# Copy only installed deps (NOT full /usr/local)
COPY --from=builder /install /usr/local

COPY . .

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://localhost:8000/health || exit 1

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
