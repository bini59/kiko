import uuid
from typing import Dict

import openai

API_URL = "https://api.openai.com/v1"


class VitoAPIError(Exception):
    pass


# In-memory storage for transcription results
_TRANSCRIPTS: Dict[str, str] = {}


def transcribe_audio(file_path: str, token: str) -> str:
    """Transcribe an audio file using OpenAI's Whisper API.

    Returns a transcript id that can later be used to fetch the result.
    """
    openai.api_key = token
    try:
        with open(file_path, "rb") as fh:
            result = openai.Audio.transcribe("whisper-1", fh)
    except Exception as exc:  # pragma: no cover - error path covered in tests
        raise VitoAPIError(str(exc)) from exc

    transcript_id = str(uuid.uuid4())
    _TRANSCRIPTS[transcript_id] = result["text"]
    return transcript_id


def get_transcription_result(transcript_id: str, token: str) -> dict:
    """Retrieve a previously created transcription result."""
    if transcript_id not in _TRANSCRIPTS:
        raise VitoAPIError("Transcript not found")
    return {"text": _TRANSCRIPTS[transcript_id]}
