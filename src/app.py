from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import os
import tempfile

import kiko_api

app = FastAPI(title="Kiko API")


class Episode(BaseModel):
    id: int
    title: str
    length: int
    audio_url: str
    script: str | None = None


fake_episodes: List[Episode] = [
    Episode(
        id=1,
        title="Sample Episode 1",
        length=300,
        audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        script="こんにちは",
    ),
    Episode(
        id=2,
        title="Sample Episode 2",
        length=420,
        audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        script="おはようございます",
    ),
]


class User(BaseModel):
    username: str
    password: str


class VocabWord(BaseModel):
    id: int
    word: str
    meaning: str
    example: str | None = None
    episode_id: int | None = None


class TextRequest(BaseModel):
    text: str


fake_vocab: List[VocabWord] = []


@app.post("/auth/signup")
@app.post("/auth/login")
def auth(user: User):
    """Mock authentication returning a fake token."""
    return {"token": "fake-token"}


@app.get("/episodes", response_model=List[Episode])
def list_episodes():
    return fake_episodes


@app.get("/episodes/{episode_id}", response_model=Episode)
def get_episode(episode_id: int):
    for ep in fake_episodes:
        if ep.id == episode_id:
            return ep
    raise HTTPException(status_code=404, detail="Episode not found")


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Receive an audio file and return a transcription id."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        transcript_id = kiko_api.transcribe_audio(
            tmp_path, os.environ.get("OPENAI_API_KEY", "")
        )
    finally:
        os.unlink(tmp_path)

    return {"transcript_id": transcript_id}


@app.get("/transcribe/{transcript_id}")
def get_transcription(transcript_id: str):
    """Return transcription result."""
    try:
        return kiko_api.get_transcription_result(
            transcript_id, os.environ.get("OPENAI_API_KEY", "")
        )
    except kiko_api.VitoAPIError:
        raise HTTPException(status_code=404, detail="Transcript not found")


@app.post("/vocab", response_model=VocabWord)
def add_vocab(word: VocabWord):
    fake_vocab.append(word)
    return word


@app.get("/vocab", response_model=List[VocabWord])
def list_vocab():
    return fake_vocab


@app.get("/vocab/{word_id}", response_model=VocabWord)
def get_vocab(word_id: int):
    for word in fake_vocab:
        if word.id == word_id:
            return word
    raise HTTPException(status_code=404, detail="Word not found")


@app.delete("/vocab/{word_id}")
def delete_vocab(word_id: int):
    for i, word in enumerate(fake_vocab):
        if word.id == word_id:
            del fake_vocab[i]
            return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Word not found")


@app.post("/translate")
def translate(req: TextRequest):
    """Translate Japanese text to English using DeepL."""
    try:
        translated = kiko_api.translate_text(
            req.text, os.environ.get("DEEPL_API_KEY", "")
        )
    except kiko_api.TranslationAPIError:
        raise HTTPException(status_code=500, detail="Translation failed")
    return {"text": translated}


@app.get("/dictionary/{word}")
def dictionary_lookup(word: str):
    """Return English meaning for a Japanese word using Jisho."""
    try:
        meaning = kiko_api.lookup_word(word)
    except kiko_api.DictionaryAPIError:
        raise HTTPException(status_code=500, detail="Lookup failed")
    return {"word": word, "meaning": meaning}
