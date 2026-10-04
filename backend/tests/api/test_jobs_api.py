from fastapi.testclient import TestClient
from app.main import app
def test_jobs_require_authentication():assert TestClient(app).get('/api/v1/jobs').status_code==401
