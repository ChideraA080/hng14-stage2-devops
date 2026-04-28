# Stage 1: install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: run app
FROM python:3.11-slim

WORKDIR /app

# create non-root user
RUN useradd -m appuser
USER appuser

# copy dependencies
COPY --from=builder /root/.local /home/appuser/.local

# copy code
COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
