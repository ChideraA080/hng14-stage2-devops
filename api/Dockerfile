# Stage 1: builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

ENV PIP_DEFAULT_TIMEOUT=300

RUN pip install --upgrade pip setuptools wheel && \
    pip install \
    --no-cache-dir \
    --default-timeout=300 \
    --retries 30 \
    --timeout 300 \
    --target=/install \
    -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim

WORKDIR /app

# security update (IMPORTANT for Trivy)
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# create non-root user
RUN useradd -m appuser

# copy dependencies
COPY --from=builder /install /install

# copy application code
COPY . .

ENV PATH=/install/bin:$PATH
ENV PYTHONPATH=/install

EXPOSE 8000

# healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
