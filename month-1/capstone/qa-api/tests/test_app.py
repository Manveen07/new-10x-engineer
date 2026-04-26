import os

from fastapi.testclient import TestClient

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from app.main import create_app


def test_root_endpoint_returns_health_message() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Month 1 QA API is running."}
