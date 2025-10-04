import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Crear engine en memoria para pruebas y sobreescribir dependencia get_db
TEST_DATABASE_URL = 'sqlite:///:memory:'
engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas en la BD de prueba
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# set test API key in env for auth dependency check
os.environ['API_KEY'] = 'testkey123'

client = TestClient(app)

def test_post_and_get():
    headers = {'x-api-key': 'testkey123'}
    msg = {
      'message_id': 't1',
      'session_id': 'sess-test',
      'content': 'prueba integración',
      'timestamp': '2025-10-02T10:00:00Z',
      'sender': 'user'
    }
    r = client.post('/api/messages', json=msg, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data['status'] == 'success'

    r2 = client.get('/api/messages/sess-test', headers=headers)
    assert r2.status_code == 200
    assert r2.json()['status'] == 'success'
    assert len(r2.json()['data']) >= 1

def test_search_param():
    headers = {'x-api-key': 'testkey123'}
    # create message with known content
    msg = {
        'message_id': 't2',
        'session_id': 'sess-search',
        'content': 'esto tiene palabra_unica',
        'timestamp': '2025-10-02T11:00:00Z',
        'sender': 'user'
    }
    client.post('/api/messages', json=msg, headers=headers)
    r = client.get('/api/messages/sess-search?search=palabra_unica', headers=headers)
    assert r.status_code == 200
    assert len(r.json()['data']) == 1
