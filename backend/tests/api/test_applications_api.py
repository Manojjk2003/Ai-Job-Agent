from fastapi.testclient import TestClient
from app.main import app
def test_applications_require_authentication():assert TestClient(app).get('/api/v1/applications').status_code==401
