from fastapi.testclient import TestClient

from app.main import create_app


def test_root_returns_running_message() -> None:
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Month 1 QA API is running."}
