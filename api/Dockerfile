# Stage 1
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

ENV PIP_DEFAULT_TIMEOUT=120

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout=120 --retries=10 --target=/install -r requirements.txt


# Stage 2
FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser

# copy dependencies
COPY --from=builder /install /install

COPY . .

ENV PATH=/install/bin:$PATH
ENV PYTHONPATH=/install

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
