from fastapi.testclient import TestClient
from app.main import app
def test_hiring_source_api_requires_authentication():assert TestClient(app).get('/api/v1/companies/00000000-0000-0000-0000-000000000000/hiring-sources').status_code==401
