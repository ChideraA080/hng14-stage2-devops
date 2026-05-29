import redis
import time
import os
import signal

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
    socket_connect_timeout=10,
    socket_timeout=10,
    retry_on_timeout=True
)

QUEUE_NAME = os.getenv("QUEUE_NAME", "jobs")

running = True


def shutdown(sig, frame):
    global running
    running = False
    print("Shutting down worker gracefully...")


signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)

    r.hset(f"job:{job_id}", mapping={
        "status": "completed"
    })

    print(f"Done: {job_id}")


while running:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)

        if job:
            _, job_id = job
            process_job(job_id)

    except redis.exceptions.ConnectionError:
        print("Redis not available, retrying...")
        time.sleep(3)

    except redis.exceptions.TimeoutError:
        # normal for BRPOP timeout — NOT a failure
        continue

    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(2)
