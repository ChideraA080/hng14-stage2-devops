
# HNG14 Stage 2-DevOps - Containerized Microservices CI/CD Pipeline

## Overview

This project is a production-ready containerized microservices system built as part of the HNG14 DevOps Stage 2 task.

It consists of three services:

- **Frontend (Node.js)** - Submits and tracks jobs
- **API (FastAPI / Python)** - Creates and manages job status
- **Worker (Python)** - Processes jobs from Redis queue
- **Redis** - Shared in-memory message broker

The entire system is fully containerized using Docker and orchestrated with Docker Compose, with a complete CI/CD pipeline using GitHub Actions.

---

## Architecture

Services communicate over a private Docker network:

- Frontend → API → Redis queue → Worker
- Worker updates job status back in Redis
- API exposes job status to frontend

Redis is NOT exposed externally for security reasons.

---

## Tech Stack

- Python (FastAPI)
- Node.js (Frontend)
- Redis
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Trivy (Security scanning)
- Hadolint (Docker linting)
- Pytest (Unit testing)

---

## Prerequisites

Before running locally:

- Docker installed → https://docs.docker.com/get-docker/
- Docker Compose installed
- Git installed

---

## How to Run Locally

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/hng14-stage2-devops.git
cd hng14-stage2-devops
```
### 2. Create Environment File

```
cp .env.example .env
```
Update values if needed:
```
REDIS_HOST=redis
REDIS_PORT=6379
QUEUE_NAME=jobs
API_URL=http://api:8000
PORT=3000
```
### 3. Build and Start Services
```
docker compose up --build
```
Accessing the Application
```
| Service    | URL                                                          |
| ---------- | ------------------------------------------------------------ |
| Frontend   | [http://localhost:3000](http://localhost:3000)               |
| API        | [http://localhost:8000](http://localhost:8000)               |
| API Health | [http://localhost:8000/health](http://localhost:8000/health) |
```
## API Health Check
```
curl http://localhost:8000/health
```
Expected response:
```
{"status": "ok"}
```
## Running Tests

Inside API container:
```
docker exec -it api pytest --cov=.
```
## CI/CD Pipeline

The GitHub Actions pipeline runs in this strict order:
```
lint → test → build → security scan → integration test → deploy
```
Pipeline Stages
1. Lint
- flake8 (Python)
- eslint (JavaScript)
- hadolint (Dockerfiles)

2. Test
- Pytest unit tests
- Redis mocked
- Coverage report uploaded as artifact

3. Build
- Builds API, Worker, Frontend images
- Tags images with:
  - latest
  - git SHA 
- Pushes to local registry (CI service container)

4. Security Scan
- Trivy scans all images
- Fails pipeline on CRITICAL vulnerabilities
- Uploads SARIF report

5. Integration Tests

- Spins up full stack in CI
- Submits job via frontend
- Verifies job processing via API
- Tears down environment safely

6. Deploy (Main branch only)

- Rolling deployment strategy
- New container must pass health checks
- If health check fails → rollback
- Docker Features

Each service includes:
- Multi-stage builds
- Non-root user execution
- HEALTHCHECK instruction
- Environment variable configuration
- No secrets inside images

### Security Considerations

- Redis is not exposed publicly
- Containers run as non-root users
- No hardcoded secrets or credentials
- Vulnerability scanning enforced in CI

### Known Design Decisions
- Redis is used as a lightweight queue system
- Workers poll Redis queue for job processing
- API and worker communicate asynchronously
- Health checks ensure container readiness before dependency startup

## FIXES Documentation

All bugs discovered in the original codebase have been documented in:
```
FIXES.md
```
Each entry includes:

- File name
- Line or section
- Problem description
- Fix applied
- Reason for fix

## Project Status

- All services containerized

- Full CI/CD pipeline implemented

- Security scanning enabled

- Integration testing implemented

- Rolling deployment configured

- Production-grade Docker setup

## Notes

This project intentionally includes real-world production issues:

- Misconfigured networking
- Missing health checks
- Dependency mismatches
- Container build inefficiencies

All issues were identified, fixed, and documented as part of the DevOps evaluation process.

## Author

Chidera Alaeto

DevOps Engineer Candidate - HNG14 Stage 2 Submission

