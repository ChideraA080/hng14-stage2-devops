# Stage 1: install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

# IMPORTANT FIX: install into a known path instead of --user
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: run app
FROM python:3.11-slim

WORKDIR /app

# create non-root user
RUN useradd -m appuser

# copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# copy app code
COPY . .

# make python see installed packages
ENV PATH=/usr/local/bin:$PATH
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

EXPOSE 8000

# health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# run as non-root user (AFTER setup)
USER appuser

# start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
