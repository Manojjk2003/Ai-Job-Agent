from fastapi.testclient import TestClient

from app.main import app


def test_health_is_public() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_auth_health_requires_bearer_token() -> None:
    response = TestClient(app).get("/health/auth")
    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"


def test_auth_health_reports_unconfigured_firebase() -> None:
    response = TestClient(app).get("/health/auth", headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 503
    assert response.json()["detail"] == "Authentication is not configured"
