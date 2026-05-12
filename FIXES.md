# Bugs Api/main.py (API Fixes) 

## Bug 1 - Hardcoded Redis Host
File: api/main.py
Line: 6 hardcoded host="localhost"
Problem: Redis host was hardcoded to "localhost", which breaks in containerized environments
Fix: Replaced with environment variables REDIS_HOST and REDIS_PORT with sensible defaults

```python
host=os.getenv("REDIS_HOST", "redis")
```
Why It Was Needed:Allows the API container to communicate correctly with the Redis container in Docker Compose and CI environments

## Bug 2 - Missing Redis Password Authentication
File:api/main.py
Line 6: no password
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Redis is configured with a password (REDIS_PASSWORD) but the client never sends it. Redis will reject every single command with NOAUTH error.
Fix: Added password support using environment variables( Add password=os.getenv("REDIS_PASSWORD", None)
Why It Was Needed:Ensures the API can authenticate successfully with secured Redis instances.

## Bug 3 - Missing decode_responses=True
File:api/main.py
Line 6: no decode_responses
pythonr = redis.Redis(host="localhost", port=6379)
Problem: Redis returned raw byte strings like b"queued" instead of normal strings. This caused unnecessary decoding logic and runtime errors.
Fix: Added decode_responses=True
Why It Was Needed: Ensures Redis responses are automatically converted into Python strings.

## Bug 4 - Queue Name Mismatch
File:api/main.py
Line 10: wrong queue name "job"
pythonr.lpush("job", job_id)

Problem: Queue name was hardcoded as "jobs"
Fix: Introduced environment variable QUEUE_NAME and replaced hardcoded value (QUEUE_NAME=os.getenv("QUEUE_NAME", "jobs")
Why It Was Needed: Ensures the API and worker communicate using the same Redis queue.

## Bug 5 - Invalid .decode() Usage
file:api/main.py
Line 18: .decode() will crash
pythonreturn {"job_id": job_id, "status": status.decode()}

Problem: Once we add decode_responses=True, Redis already returns a plain string. Calling .decode() on a string crashes with AttributeError: 'str' object has no attribute 'decode' (AttributeError: 'str' object has no attribute 'decode')
Fix: Remove .decode() — just return status directly
Why It Was Needed: Prevents runtime crashes when returning job status responses.

## Bug 6 - Missing /health Endpoint
File:api/main.py

Missing entirely: no /health endpoint

Problem: The Dockerfile HEALTHCHECK will call /health to check if the API is alive. This route does not exist so Docker always marks the container as unhealthy. All services that depend on the API (frontend, worker) will never start.
Fix: Add a /health route that returns {"status": "ok"}
```
@app.get("/health")
def health():
    return {"status": "ok"}
```
Why It Was Needed: Allows Docker and orchestration systems to verify API health correctly.

## BUG 7 Api/requirements.txt - Non-Production Uvicorn Installation
api/requirements.txt Bug Found
Bug — uvicorn missing [standard]
uvicorn

Problem: Plain uvicorn installs the minimal version with a slower event loop and no websocket support. Not suitable for production.
Fix: Change to uvicorn[standard]
Why It Was Needed: Improves production performance and stability.

## Bug 8 — Unpinned Python Dependencies

File: api/requirements.txt
Section: All dependencies
Problem:Dependencies were not pinned to fixed versions. Future package updates could break builds or introduce incompatibilities.

Fix: Pinned all dependency versions explicitly.
Why It Was Needed: Ensures reproducible builds across local development, CI pipelines, and deployments.

# Bugs frontend/app.js (Frontend Api

## Bug 9 - Hardcoded API URL
File:frontend/app.js
Bug 1 — Line 5: hardcoded API URL
javascriptconst API_URL = "http://localhost:8000";

Problem: Frontend container cannot reach the API container via localhost. They are separate containers on separate network namespaces. Every job submission will fail with connection refused.
Fix: process.env.API_URL || "http://api:8000" — reads from environment variable, falls back to Docker service name
Why It Was Needed: Allows frontend-to-API communication inside Docker networks.

## Bug 10 - Poor Error Visibility
File:frontend/app.js
Line 10 and 16: error messages hide real problem
javascriptres.status(500).json({ error: "something went wrong" });

Problem: When something fails you get "something went wrong" with zero information about what actually broke. Impossible to debug.
Fix: Log the real error and return the actual error message
Why It Was Needed: Improves debugging and operational visibility.

## Bug 11 - Hardcoded Frontend Port
File:frontend/app.js
Last line: hardcoded port 3000
javascriptapp.listen(3000, () => {

Problem: Port is hardcoded preventing flexible deployments.
Fix: process.env.PORT || 3000 — reads from environment variable
```
process.env.PORT || 3000
```
Why It Was Needed: Allows configurable runtime environments.

## Bug 12 - Missing Frontend /health Endpoint
File:frontend/app.js
Missing entirely: no /health endpoint

Problem: Docker HEALTHCHECK needs to call /health to know if the frontend container is alive. Without it the container always reports unhealthy.
Fix: Add a /health route returning {"status": "ok"}
Why It Was Needed: Allows container health monitoring and dependency checks.

# Bugs worker/worker.py (Worker Fixes)

## Bug 13 - Hardcoded Redis Host
File:worker.py
Line 5: hardcoded host="localhost"
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Same as main.py — localhost inside Docker means the worker container itself, not Redis. Worker can never connect to Redis.
Fix: Replace with os.getenv("REDIS_HOST", "redis")
Why It Was Needed: Allows worker container to communicate with Redis properly.

## Bug 14 - Missing Redis Password
File: worker.py
Line 5: no password
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Redis has a password set but worker never sends it. Every Redis command gets rejected.
Fix: Add password=os.getenv("REDIS_PASSWORD", None)
Why It Was Needed: Ensures successful Redis authentication.

## Bug 15 - Missing decode_responses=True
File: worker.py
Line 5: no decode_responses
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Without it, Redis returns raw bytes. That causes the manual job_id.decode() on line 14 which will crash if anything changes.
Fix: Add decode_responses=True and remove the manual .decode()
Why It Was Needed: Simplifies Redis response handling and prevents decoding issues.

## Bug 16 - Queue Name Mismatch
File:worker.py
Line 12: wrong queue name "job"
pythonjob = r.brpop("job", timeout=5)

Problem: Worker listens on queue "job" but API pushes to "jobs". They never talk to each other. Jobs pile up forever unprocessed.
Fix: Updated worker to use the shared queue name. Change "job" to "jobs"
Why It Was Needed: Allows jobs to be processed correctly.

## Bug 17 - Invalid .decode() Usage

File:worker.py
Line 14: manual .decode() on job_id
pythonprocess_job(job_id.decode())

Problem: Once decode_responses=True is set, job_id is already a string. Calling .decode() on it crashes with AttributeError.
Fix: Remove .decode() — use job_id directly
Why It Was Needed

Prevents runtime crashes.

## Bug 18 - Missing Graceful Shutdown Handling
File:worker.py
Missing entirely: no graceful shutdown

Problem: Docker sends SIGTERM signal when stopping a container. Without handling it, the worker's brpop call hangs and Docker force-kills it after 10 seconds — any job being processed at that moment gets lost.
Fix: Added graceful shutdown handling using:
```
signal.signal(signal.SIGTERM, shutdown)
```
Why It Was Needed: Ensures clean container shutdown and prevents interrupted jobs.


