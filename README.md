
# HNG14 Stage 2-DevOps - Containerized Microservices CI/CD Pipeline

## Overview

This project is a production-ready containerized microservices system built as part of the HNG14 DevOps Stage 2 task.

It demonstrates a complete event-driven job processing system using Redis as a message broker, fully automated with a CI/CD pipeline.

The system is fully containerized and orchestrated using Docker Compose, with automated testing, security scanning, and deployment simulation using GitHub Actions.


It consists of four components::

- **Frontend (Node.js)** - Submits and tracks jobs
- **API (FastAPI / Python)** - Creates and manages job status
- **Worker (Python)** - Processes jobs from Redis queue
- **Redis** - Shared in-memory message broker

  
## Architecture

The system follows an asynchronous event-driven architecture:

Frontend → API → Redis Queue → Worker → Redis → API → Frontend

### Flow

1. User submits a job via the Frontend
2. API generates a job ID and pushes it to Redis queue
3. Worker consumes jobs from Redis
4. Worker processes the job and updates status in Redis
5. API exposes job status via REST endpoints
6. Frontend polls API for updates

## Services

### Frontend (Node.js)
- Submits and tracks jobs
- Communicates with API

### API (FastAPI / Python)
- Creates jobs
- Manages job status
- Exposes REST endpoints

### Worker (Python)
- Processes jobs from Redis queue
- Updates job status

### Redis
- In-memory message broker
- Shared between API and Worker
- Not exposed externally

The entire system is fully containerized using Docker and orchestrated with Docker Compose, with a complete CI/CD pipeline using GitHub Actions.
       

Services communicate over a private Docker network:

- Frontend → API → Redis queue → Worker
- Worker updates job status back in Redis
- API exposes job status to frontend

Redis is NOT exposed externally for security reasons.

## Tech Stack

- Python (FastAPI)
- Node.js (Frontend)
- Redis
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Trivy (Security scanning)
- Hadolint (Docker linting)
- Pytest (Unit testing)

## Prerequisites

Before running locally:

- Docker installed → https://docs.docker.com/get-docker/
- Docker Compose installed
- Git installed

  Verify:

```bash
docker --version
docker compose version
git --version
```

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
Required Environment Variables:
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
Expected Startup Output

redis    | Ready to accept connections
api      | Application startup complete
worker   | Worker started successfully
frontend | Server running on port 3000

Verify Running ContainersAccessing the Application

```
docker ps
```
Expected:

api → Up (healthy)
worker → Up (healthy)
frontend → Up (healthy)
redis → Up (healthy)

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
Confirmation
![ Architecture Diagram](https://github.com/ChideraA080/hng-stage1/blob/main/Hng%20_Stage1%20Screenshots/Stage1%20Architceture%20Diagram.png)
End-to-End Job Flow Test

Create Job
```
curl -X POST http://localhost:8000/jobs
```
Expected:
```
{
  "job_id": "uuid"
}
```
Check Job Status
```
curl http://localhost:8000/jobs/<job_id>
```
Expected:
```
{
  "job_id": "uuid",
  "status": "completed"
}
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
- SARIF reports uploaded as artifacts

5. Integration Tests

- Spins up full stack in CI
- Submits job via API
- Polls job completion
- Validates result
- Tears down environment 

6. Deploy (Main branch only)

- Rolling deployment strategy
- New container must pass health checks
- If health check fails within 60 seconds → rollback

6. Docker Standards Implemented

Each service includes:
- Multi-stage builds
- Non-root users in all containers
- Health checks included
- Environment-based configuration
- No secrets inside images
- Internal Docker networking

### Security Considerations

- Redis not exposed externally
- Containers run as non-root users
- Vulnerability scanning enforced in CI pipeline
- No hardcoded secrets

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

- Fully containerized microservices

- Fully CI/CD pipeline implemented

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

