import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import builtins
from unittest import mock
import pytest

import kiko_api


def test_transcribe_audio_success(tmp_path):
    dummy_path = tmp_path / "audio.mp3"
    dummy_path.write_bytes(b"dummy")

    with mock.patch("requests.post") as mock_post, mock.patch.object(builtins, "open", mock.mock_open(read_data=b"dummy")):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "123"}
        transcript_id = kiko_api.transcribe_audio(str(dummy_path), "token")
        assert transcript_id == "123"
        mock_post.assert_called_once()


def test_transcribe_audio_failure(tmp_path):
    dummy_path = tmp_path / "audio.mp3"
    dummy_path.write_bytes(b"dummy")

    with mock.patch("requests.post") as mock_post, mock.patch.object(builtins, "open", mock.mock_open(read_data=b"dummy")):
        mock_post.return_value.status_code = 500
        with pytest.raises(kiko_api.VitoAPIError):
            kiko_api.transcribe_audio(str(dummy_path), "token")


def test_get_transcription_result_success():
    with mock.patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"text": "hello"}
        data = kiko_api.get_transcription_result("123", "token")
        assert data["text"] == "hello"
        mock_get.assert_called_once()


def test_get_transcription_result_failure():
    with mock.patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        with pytest.raises(kiko_api.VitoAPIError):
            kiko_api.get_transcription_result("123", "token")
