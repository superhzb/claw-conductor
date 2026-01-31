from fastapi.testclient import TestClient

from demo_project.app import app

client = TestClient(app)

def test_health() -> None:
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json() == {'ok': True}

def test_ping() -> None:
    r = client.get('/ping')
    assert r.status_code == 200
    assert r.json() == {'pong': True}
