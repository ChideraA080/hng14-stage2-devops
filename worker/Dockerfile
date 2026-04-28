# Stage 1: install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: runtime
FROM python:3.11-slim

WORKDIR /app

# create non-root user
RUN useradd -m appuser
USER appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

ENV PATH=/home/appuser/.local/bin:$PATH

# healthcheck (process must be running)
HEALTHCHECK CMD pgrep python || exit 1

CMD ["python", "worker.py"]
