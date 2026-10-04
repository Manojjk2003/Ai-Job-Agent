from fastapi.testclient import TestClient
from app.main import app

def test_communications_require_authentication():
 client=TestClient(app)
 assert client.get('/api/v1/communications').status_code==401
 assert client.get('/api/v1/integrations').status_code==401
