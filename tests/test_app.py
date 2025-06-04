import importlib
import os
import sys
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import app
import pytest

@pytest.fixture
def client():
    importlib.reload(app)
    return TestClient(app.app)

def test_auth_returns_token(client):
    resp = client.post('/auth/login', json={'username': 'u', 'password': 'p'})
    assert resp.status_code == 200
    assert resp.json()['token'] == 'fake-token'


def test_auth_validation_error(client):
    resp = client.post('/auth/login', json={})
    assert resp.status_code == 422

def test_list_episodes(client):
    resp = client.get('/episodes')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]['id'] == 1

def test_get_episode_success(client):
    resp = client.get('/episodes/1')
    assert resp.status_code == 200
    assert resp.json()['id'] == 1

def test_get_episode_not_found(client):
    resp = client.get('/episodes/999')
    assert resp.status_code == 404

def test_transcribe_endpoint(client, tmp_path):
    file_path = tmp_path / 'audio.mp3'
    file_path.write_bytes(b'test')
    with file_path.open('rb') as f:
        resp = client.post('/transcribe', files={'file': ('audio.mp3', f, 'audio/mpeg')})
    assert resp.status_code == 200
    assert resp.json()['transcript_id'] == '123'


def test_transcribe_requires_file(client):
    resp = client.post('/transcribe')
    assert resp.status_code == 422

def test_add_and_list_vocab(client):
    word = {'id': 1, 'word': 'test', 'meaning': 'meaning'}
    resp = client.post('/vocab', json=word)
    assert resp.status_code == 200
    assert resp.json() == word
    resp = client.get('/vocab')
    assert resp.status_code == 200
    assert word in resp.json()


def test_vocab_validation_error(client):
    resp = client.post('/vocab', json={'id': 1, 'word': 'test'})
    assert resp.status_code == 422
