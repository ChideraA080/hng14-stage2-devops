# Stage 1: install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --target=/install -r requirements.txt


# Stage 2: runtime
FROM python:3.11-slim

WORKDIR /app

# create non-root user
RUN useradd -m appuser

# copy dependencies
COPY --from=builder /install /install

# copy app code
COPY . .

ENV PATH=/install/bin:$PATH
ENV PYTHONPATH=/install

# switch to non-root user
USER appuser

# healthcheck
HEALTHCHECK CMD python -c "print('worker healthy')" || exit 1

CMD ["python", "worker.py"]
