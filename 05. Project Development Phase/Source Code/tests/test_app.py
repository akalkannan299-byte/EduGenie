from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_home():
    r=client.get('/'); assert r.status_code==200 and 'EduGenie' in r.text
def test_health():
    r=client.get('/health'); assert r.status_code==200 and r.json()['service']=='EduGenie'
def test_validation():
    r=client.post('/qa',json={'text':'x'}); assert r.status_code==422
def test_docs():
    assert client.get('/docs').status_code==200
