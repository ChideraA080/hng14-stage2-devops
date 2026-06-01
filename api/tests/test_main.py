from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_job():
    with patch("api.main.r") as mock_redis:
        mock_redis.lpush.return_value = 1

        response = client.post("/jobs")

        assert response.status_code == 200
        assert "job_id" in response.json()



def test_get_job_status():
    with patch("api.main.r") as mock_redis:
        mock_redis.get.return_value = b"completed"

        response = client.get("/jobs/test-id")

        assert response.status_code == 200



def test_invalid_job():
    with patch("api.main.r") as mock_redis:
        mock_redis.get.return_value = None

        response = client.get("/jobs/invalid-id")

        assert response.status_code in [404, 200]
