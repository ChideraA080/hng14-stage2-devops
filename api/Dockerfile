# Stage 1: builder
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

ENV PIP_DEFAULT_TIMEOUT=600
ENV PIP_RETRIES=20
ENV PIP_TIMEOUT=600

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install \
    --no-cache-dir \
    --default-timeout=600 \
    --retries 20 \
    --timeout 600 \
    --prefer-binary \
    --target=/install \
    -r requirements.txt

# Stage 2: runtime
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

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
