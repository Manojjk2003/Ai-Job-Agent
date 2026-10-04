from fastapi.testclient import TestClient
from app.main import app
def test_analytics_require_authentication():assert TestClient(app).get('/api/v1/analytics/overview').status_code==401
