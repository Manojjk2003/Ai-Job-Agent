from fastapi.testclient import TestClient
from app.main import app
def test_contacts_and_outreach_require_authentication():
 client=TestClient(app);assert client.get('/api/v1/outreach').status_code==401;assert client.get('/api/v1/companies/00000000-0000-0000-0000-000000000000/contacts').status_code==401
