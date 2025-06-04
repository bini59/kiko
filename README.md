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

## Running the API server

This repository includes a small FastAPI application exposing the basic endpoints proposed in the PRD. To start the development server run:

```bash
uvicorn src.app:app --reload
```
