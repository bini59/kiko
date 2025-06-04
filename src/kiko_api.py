import uuid
from typing import Dict

import openai
import requests

API_URL = "https://api.openai.com/v1"


class VitoAPIError(Exception):
    pass


class TranslationAPIError(Exception):
    """Raised when translation fails."""
    pass


class DictionaryAPIError(Exception):
    """Raised when dictionary lookup fails."""
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


def translate_text(text: str, token: str, source_lang: str = "JA", target_lang: str = "EN") -> str:
    """Translate text using the DeepL API."""
    if not token:
        raise TranslationAPIError("Missing API key")
    url = "https://api-free.deepl.com/v2/translate"
    try:
        resp = requests.post(
            url,
            data={
                "auth_key": token,
                "text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["translations"][0]["text"]
    except Exception as exc:
        raise TranslationAPIError(str(exc)) from exc


def lookup_word(word: str) -> str:
    """Look up a Japanese word via the Jisho API and return its first English definition."""
    url = "https://jisho.org/api/v1/search/words"
    try:
        resp = requests.get(url, params={"keyword": word}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("data"):
            raise DictionaryAPIError("No results")
        entry = data["data"][0]
        meaning = entry["senses"][0]["english_definitions"][0]
        return meaning
    except Exception as exc:
        raise DictionaryAPIError(str(exc)) from exc
