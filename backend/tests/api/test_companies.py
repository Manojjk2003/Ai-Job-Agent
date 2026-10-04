from fastapi.testclient import TestClient

from app.main import app


def test_company_endpoints_require_authentication():
    client = TestClient(app)
    assert client.get("/api/v1/companies").status_code == 401
    assert client.post("/api/v1/companies/discover", json={"location": {"location_name": "Bengaluru"}}).status_code == 401
