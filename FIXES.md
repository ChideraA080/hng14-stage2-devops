# Bugs Api/main.py 

## Bug 1
File: api/main.py
Line: 6 hardcoded host="localhost"
Problem: Redis host was hardcoded to "localhost", which breaks in containerized environments
Fix: Replaced with environment variables REDIS_HOST and REDIS_PORT with sensible defaults

## Bug 2 
File:api/main.py
Line 6: no password
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Redis is configured with a password (REDIS_PASSWORD) but the client never sends it. Redis will reject every single command with NOAUTH error.
Fix: Add password=os.getenv("REDIS_PASSWORD", None)

## Bug 3 
File:api/main.py
Line 6: no decode_responses
pythonr = redis.Redis(host="localhost", port=6379)

## Api
Main.py
Problem: Without decode_responses=True, Redis returns raw bytes like b"queued" instead of clean strings like "queued". This causes the .decode() crash on line 18.
Fix: Add decode_responses=True

## Bug 4
File:api/main.py
Line 10: wrong queue name "job"
pythonr.lpush("job", job_id)

Problem: API pushes jobs into a queue called "job" but the worker listens on a queue called "jobs". Jobs go in and never come out — worker never sees them.
Fix: Change "job" to "jobs"

## Bug 5
file:api/main.py
Line 18: .decode() will crash
pythonreturn {"job_id": job_id, "status": status.decode()}

Problem: Once we add decode_responses=True, Redis already returns a plain string. Calling .decode() on a string crashes with AttributeError: 'str' object has no attribute 'decode'
Fix: Remove .decode() — just return status directly

### Bug 6
File:api/main.py

Missing entirely: no /health endpoint

Problem: The Dockerfile HEALTHCHECK will call /health to check if the API is alive. This route does not exist so Docker always marks the container as unhealthy. All services that depend on the API (frontend, worker) will never start.
Fix: Add a /health route that returns {"status": "ok"}

# Api/requirements.txt
api/requirements.txt Bug Found
Bug — uvicorn missing [standard]
uvicorn

Problem: Plain uvicorn installs the minimal version with a slower event loop and no websocket support. Not suitable for production.
Fix: Change to uvicorn[standard]

# Bugs frontend/app.js 

## Bug 1
File:frontend/app.js
Bug 1 — Line 5: hardcoded API URL
javascriptconst API_URL = "http://localhost:8000";

Problem: Frontend container cannot reach the API container via localhost. They are separate containers on separate network namespaces. Every job submission will fail with connection refused.
Fix: process.env.API_URL || "http://api:8000" — reads from environment variable, falls back to Docker service name

## Bug 2
File:frontend/app.js
Line 10 and 16: error messages hide real problem
javascriptres.status(500).json({ error: "something went wrong" });

Problem: When something fails you get "something went wrong" with zero information about what actually broke. Impossible to debug.
Fix: Log the real error and return the actual error message

## Bug 3
File:frontend/app.js
Last line: hardcoded port 3000
javascriptapp.listen(3000, () => {

Problem: Port is hardcoded. In production or different environments you cannot change it without editing the source code.
Fix: process.env.PORT || 3000 — reads from environment variable

## Bug 4
File:frontend/app.js
Missing entirely: no /health endpoint

Problem: Docker HEALTHCHECK needs to call /health to know if the frontend container is alive. Without it the container always reports unhealthy.
Fix: Add a /health route returning {"status": "ok"}

# Bugs worker/worker.py

## Bug 1
File:worker.py
Line 5: hardcoded host="localhost"
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Same as main.py — localhost inside Docker means the worker container itself, not Redis. Worker can never connect to Redis.
Fix: Replace with os.getenv("REDIS_HOST", "redis")

## Bug 2
File: worker.py
Line 5: no password
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Redis has a password set but worker never sends it. Every Redis command gets rejected.
Fix: Add password=os.getenv("REDIS_PASSWORD", None)

## Bug 3
File: worker.py
Line 5: no decode_responses
pythonr = redis.Redis(host="localhost", port=6379)

Problem: Without it, Redis returns raw bytes. That causes the manual job_id.decode() on line 14 which will crash if anything changes.
Fix: Add decode_responses=True and remove the manual .decode()

## Bug 4
File:worker.py
Line 12: wrong queue name "job"
pythonjob = r.brpop("job", timeout=5)

Problem: Worker listens on queue "job" but API pushes to "jobs". They never talk to each other. Jobs pile up forever unprocessed.
Fix: Change "job" to "jobs"

## Bug 5
File:worker.py
Line 14: manual .decode() on job_id
pythonprocess_job(job_id.decode())

Problem: Once decode_responses=True is set, job_id is already a string. Calling .decode() on it crashes with AttributeError.
Fix: Remove .decode() — use job_id directly

## Bug 6
File:worker.py
Missing entirely: no graceful shutdown

Problem: Docker sends SIGTERM signal when stopping a container. Without handling it, the worker's brpop call hangs and Docker force-kills it after 10 seconds — any job being processed at that moment gets lost.
Fix: Add signal.signal(SIGTERM, shutdown) with a running flag so the loop exits cleanly

 
