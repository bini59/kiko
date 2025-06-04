import requests

API_URL = "https://openapi.vito.ai/v1"

class VitoAPIError(Exception):
    pass


def transcribe_audio(file_path: str, token: str) -> str:
    """Upload an audio file for transcription.

    Returns the transcription id.
    """
    url = f"{API_URL}/transcribe"
    headers = {"Authorization": f"Bearer {token}"}
    files = {
        "file": open(file_path, "rb"),
        "config": (
            None,
            '{"model_name": "whisper", "language": "ja"}',
            "application/json",
        ),
    }
    response = requests.post(url, files=files, headers=headers)
    if response.status_code != 200:
        raise VitoAPIError(f"Unexpected status {response.status_code}")
    data = response.json()
    return data["id"]


def get_transcription_result(transcript_id: str, token: str) -> dict:
    """Get the transcription result given an id."""
    url = f"{API_URL}/transcribe/{transcript_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise VitoAPIError(f"Unexpected status {response.status_code}")
    return response.json()
