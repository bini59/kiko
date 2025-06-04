from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Kiko API")


class Episode(BaseModel):
    id: int
    title: str
    length: int
    script: str | None = None


fake_episodes: List[Episode] = [
    Episode(id=1, title="Sample Episode", length=300, script="こんにちは"),
]


class User(BaseModel):
    username: str
    password: str


class VocabWord(BaseModel):
    id: int
    word: str
    meaning: str


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
    """Receive an audio file and return a transcription id (mock)."""
    # In a real implementation this would store the file and invoke the STT service.
    return {"transcript_id": "123"}


@app.get("/transcribe/{transcript_id}")
def get_transcription(transcript_id: str):
    """Return transcription result (mock)."""
    # Placeholder: call to external STT service
    result = {
        "text": "dummy text"
    }
    return result


@app.post("/vocab", response_model=VocabWord)
def add_vocab(word: VocabWord):
    fake_vocab.append(word)
    return word


@app.get("/vocab", response_model=List[VocabWord])
def list_vocab():
    return fake_vocab
