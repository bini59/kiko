import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import builtins
from unittest import mock
import pytest

import kiko_api


def test_transcribe_audio_success(tmp_path):
    dummy_path = tmp_path / "audio.mp3"
    dummy_path.write_bytes(b"dummy")

    with mock.patch("kiko_api.openai.Audio.transcribe") as mock_transcribe, \
         mock.patch.object(builtins, "open", mock.mock_open(read_data=b"dummy")):
        mock_transcribe.return_value = {"text": "hello"}
        transcript_id = kiko_api.transcribe_audio(str(dummy_path), "token")
        assert transcript_id in kiko_api._TRANSCRIPTS
        assert kiko_api._TRANSCRIPTS[transcript_id] == "hello"
        mock_transcribe.assert_called_once()


def test_transcribe_audio_failure(tmp_path):
    dummy_path = tmp_path / "audio.mp3"
    dummy_path.write_bytes(b"dummy")

    with mock.patch("kiko_api.openai.Audio.transcribe") as mock_transcribe, \
         mock.patch.object(builtins, "open", mock.mock_open(read_data=b"dummy")):
        mock_transcribe.side_effect = Exception("fail")
        with pytest.raises(kiko_api.VitoAPIError):
            kiko_api.transcribe_audio(str(dummy_path), "token")


def test_get_transcription_result_success():
    kiko_api._TRANSCRIPTS.clear()
    kiko_api._TRANSCRIPTS["123"] = "hello"
    data = kiko_api.get_transcription_result("123", "token")
    assert data["text"] == "hello"


def test_get_transcription_result_failure():
    with pytest.raises(kiko_api.VitoAPIError):
        kiko_api.get_transcription_result("nope", "token")


def test_translate_text_success(monkeypatch):
    def fake_post(url, data, timeout):
        class Resp:
            def raise_for_status(self):
                pass

            def json(self):
                return {"translations": [{"text": "hello"}]}

        assert data["text"] == "こんにちは"
        return Resp()

    monkeypatch.setattr(kiko_api.requests, "post", fake_post)
    text = kiko_api.translate_text("こんにちは", "token")
    assert text == "hello"


def test_translate_text_failure(monkeypatch):
    def fake_post(url, data, timeout):
        raise Exception("boom")

    monkeypatch.setattr(kiko_api.requests, "post", fake_post)
    with pytest.raises(kiko_api.TranslationAPIError):
        kiko_api.translate_text("hi", "token")
