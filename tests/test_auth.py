from fastapi.testclient import TestClient
from fastapi import status
import src.app as app_module
from src.models.users import User

class _DummyConn:
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        pass
    
    async def run_sync(self, fn, *args, **kwargs):
        return None
    
class _DummyEngine:
    def begin(self):
        return _DummyConn()
    
    async def dispose(self):
        pass
    
class _DummyBase:
    class _Meta:
        def create_all(self, *args, **kwargs):
            return None
    
    metadata = _Meta()
    
def _setup_minimal_lifespan(monkeypatch):
    monkeypatch.setattr(app_module, "engine", _DummyEngine())
    monkeypatch.setattr(app_module, "Base", _DummyBase())
    
def test_token_success(monkeypatch):
    _setup_minimal_lifespan(monkeypatch)
    
    async def fake_get_by_email(email, db):
        return User(email=email, password="hashed")
    
    async def fake_get_session():
        class DummySession:
            pass
        return DummySession()
    
    monkeypatch.setattr(app_module, "get_by_email", fake_get_by_email)
    monkeypatch.setattr(app_module, "get_session", fake_get_session)
    monkeypatch.setattr(app_module, "verify_password", lambda pw, hashed: True)
    monkeypatch.setattr(app_module, "create_access_token", lambda data: "fake-token")
    
    client = TestClient(app_module.app)
    resp = client.post("/token", data={"username": "user@example.com", "password": "secret"})
    assert resp.status_code == 200
    assert resp.json() == {"access_token": "fake-token", "token_type": "bearer"}


def test_token_user_not_found(monkeypatch):
    _setup_minimal_lifespan(monkeypatch)
    
    async def fake_get_by_email(email, db):
        return None
    
    async def fake_get_session():
        return object()
    
    monkeypatch.setattr(app_module, "get_by_email", fake_get_by_email)
    monkeypatch.setattr(app_module, "get_session", fake_get_session)
    
    client = TestClient(app_module.app)
    resp = client.post("/token", data={"username": "nope@example.com", "password": "x"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    
    
def test_read_root_authenticated(monkeypatch):
    _setup_minimal_lifespan(monkeypatch)
    
    user = {"id": 1, "email": "auth@example.com"}
    app_module.app.dependency_overrides[app_module.get_current_user] = lambda: user
    
    client = TestClient(app_module.app)
    resp = client.get("/", headers={"Authorization": "Bearer fake"})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == user
    
    # cleanup
    app_module.app.dependency_overrides.pop(app_module.get_current_user, None)
    
def test_read_root_unauthenticated(monkeypatch):
    _setup_minimal_lifespan(monkeypatch)
    
    app_module.app.dependency_overrides[app_module.get_current_user] = lambda: None
    
    client = TestClient(app_module.app)
    resp = client.get("/", headers={"Authorization": "Bearer fake"})
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    
    app_module.app.dependency_overrides.pop(app_module.get_current_user, None)