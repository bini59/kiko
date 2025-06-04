import importlib
import os
import sys
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import app
import kiko_api
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
    assert 'audio_url' in data[0]

def test_get_episode_success(client):
    resp = client.get('/episodes/1')
    assert resp.status_code == 200
    data = resp.json()
    assert data['id'] == 1
    assert 'audio_url' in data

def test_get_episode_not_found(client):
    resp = client.get('/episodes/999')
    assert resp.status_code == 404

def test_transcribe_endpoint(client, tmp_path, monkeypatch):
    file_path = tmp_path / 'audio.mp3'
    file_path.write_bytes(b'test')

    def fake_transcribe(model, fh):
        return {"text": "hello"}

    monkeypatch.setattr("kiko_api.openai.Audio.transcribe", fake_transcribe)

    with file_path.open('rb') as f:
        resp = client.post('/transcribe', files={'file': ('audio.mp3', f, 'audio/mpeg')})
    assert resp.status_code == 200
    transcript_id = resp.json()['transcript_id']
    assert transcript_id
    resp2 = client.get(f'/transcribe/{transcript_id}')
    assert resp2.status_code == 200
    assert resp2.json()['text'] == 'hello'


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


def test_translate_endpoint(client, monkeypatch):
    def fake_translate(text, token):
        assert text == "こんにちは"
        return "hello"

    monkeypatch.setattr("kiko_api.translate_text", fake_translate)
    resp = client.post('/translate', json={'text': 'こんにちは'})
    assert resp.status_code == 200
    assert resp.json()['text'] == 'hello'


def test_translate_failure(client, monkeypatch):
    def fail_translate(text, token):
        raise kiko_api.TranslationAPIError("boom")

    monkeypatch.setattr("kiko_api.translate_text", fail_translate)
    resp = client.post('/translate', json={'text': 'こんにちは'})
    assert resp.status_code == 500


def test_dictionary_endpoint_success(client, monkeypatch):
    def fake_lookup(word):
        assert word == "こんにちは"
        return "hello"

    monkeypatch.setattr(kiko_api, "lookup_word", fake_lookup)
    resp = client.get('/dictionary/こんにちは')
    assert resp.status_code == 200
    data = resp.json()
    assert data["meaning"] == "hello"


def test_dictionary_endpoint_failure(client, monkeypatch):
    def fail_lookup(word):
        raise kiko_api.DictionaryAPIError("boom")

    monkeypatch.setattr(kiko_api, "lookup_word", fail_lookup)
    resp = client.get('/dictionary/test')
    assert resp.status_code == 500
