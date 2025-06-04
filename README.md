# Kiko TDD Example

This project demonstrates starting test-driven development (TDD) for the Kiko application.

## Setup

```bash
pip install -r requirements.txt
```

## Running tests

```bash
pytest
```

## Test plan

The file [docs/test_plan.md](docs/test_plan.md) describes the PRD-based test categories and the criteria used to verify each feature.

## API documentation

See [docs/api_interface.md](docs/api_interface.md) for details on the available FastAPI endpoints.
The API now includes a dictionary lookup endpoint using Jisho for word meanings.

## Running the API server

This repository includes a small FastAPI application exposing the basic endpoints proposed in the PRD. To start the development server run:

```bash
uvicorn src.app:app --reload
```

The speech-to-text endpoints use OpenAI Whisper. Set the `OPENAI_API_KEY` environment
variable before launching the server to enable transcription functionality.

Translations require a DeepL API key set in `DEEPL_API_KEY`.

## Frontend development

The `frontend` directory contains a simple Svelte application displaying the
episode list and an audio player. To start the frontend dev server run:

```bash
cd frontend
npm install
npm run dev
```

The build output is written to `frontend/dist`.
