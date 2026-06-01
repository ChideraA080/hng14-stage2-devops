FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

COPY --from=builder /install /usr/local
COPY . .

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/app

USER appuser

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://api:8000/health || exit 1

CMD ["python", "worker.py"]
