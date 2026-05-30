# Stage 1: builder
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install \
    --no-cache-dir \
    --prefer-binary \
    --disable-pip-version-check \
    --target=/install \
    -r requirements.txt


# Stage 2: runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install only minimal security patches (avoid full upgrade)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser

COPY --from=builder /install /install
COPY . .

ENV PATH=/install/bin:$PATH
ENV PYTHONPATH=/install

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://localhost:8000/health || exit 1

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
