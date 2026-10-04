# Career Agent

An AI-assisted job discovery and application platform. This repository is a modular monolith: Angular provides the client, FastAPI owns application APIs, PostgreSQL is the system of record, and Qdrant is reserved for retrieval.

## Local development

1. Copy `.env.example` to `backend/.env`. Keep Firebase service-account credentials outside this repository and set `FIREBASE_CREDENTIALS_PATH` when Firebase is configured.
2. Start infrastructure: `docker compose up -d`.
3. In `backend`, create/activate a virtual environment, install with `pip install -e .`, then run `alembic upgrade head` and `uvicorn app.main:app --reload`.
4. In `frontend/career-agent-ui`, run `npm start`.

The API health endpoints are `/health` and `/health/db`; versioned application APIs start at `/api/v1`.

## Current scope

Implemented: repository bootstrap, PostgreSQL/Alembic foundation, Firebase-token verification boundary, and authenticated candidate onboarding. Resume, skills, roles, job discovery, RAG, agents, and applications are intentionally out of scope until their later approved phases.
