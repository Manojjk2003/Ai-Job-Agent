1. Purpose

Phase 9 converts the architecture from previous phases into an actual development environment.

We are not building the full product yet.

The objective is to create a clean, industry-standard foundation where we can start implementing the MVP feature-by-feature in Phase 10.

The setup must support:

Angular frontend
FastAPI backend
PostgreSQL
Alembic migrations
Firebase Authentication
Qdrant
Local Hugging Face embeddings
Gemini
Docker
Git/GitHub
Automated testing
Environment configuration
Documentation
2. Technology Stack
Frontend
Angular
TypeScript
Angular Material
Tailwind CSS
Backend
Python
FastAPI
SQLAlchemy 2.x
Pydantic
Pydantic Settings
Alembic
httpx
pytest
Authentication
Firebase Authentication
Firebase Admin SDK
Database
PostgreSQL
Vector Database
Qdrant
AI
Gemini
Google ADK
Embeddings
Hugging Face
Local embedding model
Document Processing
PyMuPDF
python-docx
Infrastructure
Docker
Docker Compose
Git
GitHub
3. Repository Strategy

The project should use a monorepo.

career-agent/
│
├── frontend/
├── backend/
├── docs/
├── infrastructure/
├── scripts/
├── tests/
├── .gitignore
├── .env.example
├── docker-compose.yml
└── README.md

Why monorepo?

Because the MVP has tightly connected frontend, backend and infrastructure.

It makes it easier to:

develop locally
version architecture documentation
keep frontend/backend changes together
reproduce the development environment
use Codex effectively

We can split services later if there is a real reason.

4. Final Initial Repository

The initial repository should look approximately like:

career-agent/
│
├── frontend/
│   └── career-agent-ui/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── alembic/
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── README.md
│
├── docs/
│   ├── phase-00-requirements.md
│   ├── phase-01-product-flows-and-use-cases.md
│   ├── phase-02-hld.md
│   ├── phase-03-database-erd.md
│   ├── phase-04-backend-lld.md
│   ├── phase-05-api-contracts.md
│   ├── phase-06-agent-tool-mcp-architecture.md
│   ├── phase-07-rag-vector-architecture.md
│   ├── phase-08-security-architecture.md
│   └── phase-09-project-setup.md
│
├── infrastructure/
│   ├── docker/
│   └── postgres/
│
├── scripts/
│
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
5. Frontend Structure

The Angular application should eventually follow:

frontend/career-agent-ui/
│
├── src/
│   ├── app/
│   │   ├── core/
│   │   ├── shared/
│   │   ├── features/
│   │   ├── layout/
│   │   ├── app.routes.ts
│   │   └── app.config.ts
│   │
│   ├── assets/
│   ├── environments/
│   ├── styles.css
│   ├── index.html
│   └── main.ts
│
├── angular.json
├── package.json
├── tsconfig.json
└── README.md
6. Angular Architecture

The frontend should not become one giant collection of components.

Use:

core/

for application-wide functionality.

Example:

core/
├── auth/
├── guards/
├── interceptors/
├── services/
├── models/
└── config/

Use:

shared/

for reusable UI components and utilities.

Use:

features/

for actual product functionality.

Example:

features/
├── onboarding/
├── profile/
├── resumes/
├── companies/
├── jobs/
├── matching/
├── applications/
└── assistant/
7. Backend Structure

The backend follows the Phase 4 LLD.

backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   └── v1/
│   │
│   ├── core/
│   ├── db/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── providers/
│   ├── agents/
│   ├── vector/
│   ├── background/
│   └── utils/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── alembic/
├── alembic.ini
├── pyproject.toml
└── README.md

We should create directories gradually rather than generating hundreds of empty files.

8. Backend Dependency Strategy

The backend should use a modern Python dependency configuration.

pyproject.toml will define:

FastAPI
Uvicorn
SQLAlchemy
psycopg
Alembic
Pydantic
pydantic-settings
httpx
Firebase Admin
pytest

AI/vector/document dependencies can be added when their respective features are implemented.

This avoids installing everything on Day 1 unnecessarily.

9. Python Environment

Use a virtual environment for local development.

Example:

backend/
    .venv/

The .venv directory must never be committed.

Add it to:

.gitignore
10. Backend Entry Point

Initial application:

backend/app/main.py

Its responsibility should initially be very small.

Conceptually:

from fastapi import FastAPI

app = FastAPI(
    title="Career Agent API",
    version="0.1.0",
)

Then expose:

GET /health

The first objective is simply:

FastAPI starts
        ↓
/health works
11. API Versioning

Use:

/api/v1/

from the beginning.

Example:

GET /api/v1/jobs
GET /api/v1/companies
GET /api/v1/resumes

This allows future versions:

/api/v2/

without breaking the existing API.

12. Health Endpoint

The first endpoint should be:

GET /health

Response:

{
  "status": "ok"
}

Later we can add:

GET /health
GET /health/ready
GET /health/live

But the MVP can begin with one simple health endpoint.

13. PostgreSQL

PostgreSQL is the primary application database.

Development setup:

Docker
  ↓
PostgreSQL container
  ↓
FastAPI

Example development configuration:

Host: localhost
Port: 5432
Database: career_agent

The exact username/password should come from environment variables.

14. Why PostgreSQL Is Local

For MVP development, PostgreSQL should run locally.

Benefits:

no cloud cost
fast development
predictable environment
easy database reset
easy Docker setup

Later:

Local PostgreSQL
        ↓
Managed PostgreSQL

when production deployment is justified.

15. Qdrant

Qdrant will also run locally through Docker.

Architecture:

FastAPI
   ↓
Retrieval Service
   ↓
Qdrant

The Angular application never communicates directly with Qdrant.

16. Docker Compose

The initial Docker Compose environment can contain:

services:

postgres
qdrant

We don't necessarily need to containerize the Angular development server or FastAPI development server immediately.

During local development:

Angular → npm/ng
FastAPI → uvicorn
PostgreSQL → Docker
Qdrant → Docker

This gives a fast development loop.

17. Initial Docker Architecture
Developer Machine
│
├── Angular
│   └── localhost:4200
│
├── FastAPI
│   └── localhost:8000
│
├── PostgreSQL
│   └── localhost:5432
│
└── Qdrant
    └── localhost:6333

Later we can containerize the whole application.

18. Environment Configuration

Environment-specific configuration must not be hard-coded.

Use:

.env

for local values.

And:

.env.example

for documentation.

Example:

ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg://...

FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=

GEMINI_API_KEY=

QDRANT_URL=http://localhost:6333

OBJECT_STORAGE_BUCKET=

LOG_LEVEL=INFO
19. Configuration Class

Backend configuration should use Pydantic Settings.

Conceptually:

Environment Variables
        ↓
Settings
        ↓
Application

Instead of:

DATABASE_URL = "postgresql://..."

inside arbitrary source files.

This gives us centralized configuration.

20. Firebase Setup

Firebase has two different responsibilities.

Client side

Angular uses Firebase Authentication.

Angular
 ↓
Firebase Auth
Server side

FastAPI uses Firebase Admin SDK.

FastAPI
 ↓
Firebase Admin SDK
 ↓
Verify Firebase ID Token

The Admin SDK credentials remain backend-only.

21. Firebase Project

Create/use a Firebase project for the application.

Enable only the authentication providers needed initially.

For MVP:

Email/password

can be sufficient.

Google login can be added later.

22. Firebase Client Configuration

Angular needs Firebase client configuration.

This configuration is not equivalent to a private secret.

Firebase client configuration is designed to be used by the client application, but backend administrative credentials must remain private.

Never expose:

Firebase Admin private key

to Angular.

23. Gemini Configuration

Gemini is the initial LLM provider.

The backend should access Gemini.

Angular
   ↓
FastAPI
   ↓
Agent / AI Service
   ↓
Gemini

Not:

Angular
   ↓
Gemini API key
   ↓
Gemini

The API key must stay server-side.

24. AI Provider Abstraction

Even though Gemini is the first provider, don't tightly couple every service to Gemini.

Use an abstraction:

LLMProvider
    │
    └── GeminiProvider

Later:

LLMProvider
    ├── GeminiProvider
    ├── OpenAIProvider
    └── LocalModelProvider

The application should depend on the interface, not directly on one vendor.

25. Embedding Provider

Similarly:

EmbeddingProvider
       │
       └── HuggingFaceEmbeddingProvider

Later:

EmbeddingProvider
    ├── HuggingFaceEmbeddingProvider
    ├── GeminiEmbeddingProvider
    └── OtherProvider

This follows the provider abstraction already established in earlier phases.

26. Google ADK

Google ADK belongs in the agent layer.

FastAPI
   ↓
Agent Orchestrator
   ↓
Google ADK
   ↓
Agents
   ↓
Tools
   ↓
Services / Providers

ADK should not become the entire backend architecture.

The application remains:

FastAPI
+
Services
+
Repositories
+
Providers
+
Agents
27. MCP

MCP is introduced at the integration/tool boundary.

It should not mean:

Everything → MCP

Instead:

Agent
  ↓
Tool interface
  ↓
Provider / MCP integration
  ↓
External system

Use MCP where it provides a meaningful integration boundary.

28. Git Strategy

Initialize Git at the repository root.

career-agent/
    .git/

Initial branches:

main
develop

For feature work:

feature/<feature-name>

Example:

feature/candidate-onboarding
feature/resume-upload
feature/job-discovery

For a solo MVP, we can keep the branching strategy lightweight.

29. Commit Strategy

Avoid commits like:

changes
updates
final
done

Prefer:

feat: add candidate profile API
feat: add resume upload validation
fix: prevent cross-candidate resume access
docs: add database architecture
test: add candidate ownership tests

This makes the repository easier to understand professionally.

30. .gitignore

At minimum:

.env
.env.*
!.env.example

.venv/
__pycache__/
*.pyc

node_modules/

dist/
build/

.angular/

.pytest_cache/

.coverage

.idea/
.vscode/

*.log

Any generated/private credentials or local database files must also be excluded.

31. README

The root README should explain:

Project
Purpose
Architecture
Technology stack
Repository structure
Local setup
Environment variables
Running frontend
Running backend
Running Docker services
Testing
Documentation

The README should be written for a new developer joining the project.

32. Development Commands

The project should eventually have predictable commands.

Backend
cd backend
python -m venv .venv

Activate the environment.

Windows:

.venv\Scripts\activate

Then:

pip install -e .

Run:

uvicorn app.main:app --reload
33. Frontend

From:

frontend/career-agent-ui

Install:

npm install

Run:

npm start

or the configured Angular development command.

Expected:

http://localhost:4200
34. Docker Services

From repository root:

docker compose up -d

This should start:

PostgreSQL
Qdrant

Check:

docker compose ps

Stop:

docker compose down
35. Initial System Test

After setup:

Angular
  ↓
loads application

FastAPI
  ↓
GET /health
  ↓
200 OK

PostgreSQL
  ↓
reachable

Qdrant
  ↓
reachable

Firebase
  ↓
authentication configured

We should not proceed to feature development until this foundation works.

36. Database Migration Setup

Alembic manages schema changes.

Flow:

SQLAlchemy Models
        ↓
Alembic Migration
        ↓
PostgreSQL

Example:

alembic revision --autogenerate -m "create candidate tables"

Then:

alembic upgrade head

Never manually modify production database schemas without migration tracking.

37. Migration Principle

Every schema change should be represented by a migration.

Example:

Migration 001
Create candidate

Migration 002
Create candidate_profile

Migration 003
Create skills

Migration 004
Create companies/jobs

This provides reproducibility.

38. Initial Database Scope

Do not create every table from Phase 3 immediately.

Phase 10 will implement features incrementally.

The first database slice should likely be:

candidate
candidate_profile
role_profile
skill
candidate_skill

Then resume-related tables.

Then jobs.

Then applications.

This keeps the first implementation understandable.

39. Testing Setup

Backend:

pytest

Test structure:

tests/
├── unit/
├── integration/
└── api/

Examples:

unit/
    test_normalization.py

integration/
    test_candidate_repository.py

api/
    test_candidate_api.py

Frontend should use Angular's supported testing setup.

40. First Tests

Before building complicated functionality, establish:

Health endpoint test
Configuration test
Database connection test
Authentication dependency test

Then feature-specific tests will be added.

41. Logging Setup

Centralize logging.

Example structure:

app/core/logging.py

Logs should include:

timestamp
level
request_id
operation
status

For agent runs:

agent_run_id
tool_call_id

where appropriate.

42. Request ID

Each API request should eventually have a request identifier.

Example:

X-Request-ID: abc123

This makes debugging much easier.

Example:

Frontend error
      ↓
request_id=abc123
      ↓
FastAPI logs
      ↓
Service logs
      ↓
Database/agent logs
43. CORS Development Setup

During local development:

Angular
localhost:4200
        ↓
FastAPI
localhost:8000

FastAPI should explicitly allow the Angular development origin.

Production origins will be configured separately.

44. Initial Directory Creation

We should create the repository progressively.

Step 1
career-agent/
Step 2
frontend/
backend/
docs/
infrastructure/
scripts/
tests/
Step 3

Create frontend application.

Step 4

Create FastAPI application.

Step 5

Start PostgreSQL.

Step 6

Start Qdrant.

Step 7

Configure Firebase.

Step 8

Configure environment.

Step 9

Create database connection.

Step 10

Create health checks.

45. What Codex Should Do

Codex should be given small, bounded tasks.

Good instruction:

Create the initial FastAPI backend structure described in
docs/phase-09-project-setup.md.

Only create:
- app/main.py
- app/core/config.py
- app/api/router.py
- app/api/v1/router.py
- health endpoint
- pyproject.toml

Do not implement business logic.
Do not create database models.
Do not create agents.
Do not modify frontend.
Run the backend tests and explain what changed.

This is much better than:

Build the entire career agent application.
46. Definition of Done for Setup

Phase 9 is complete when:

[x] Git repository initialized
[x] Monorepo structure created
[x] Angular application created
[x] FastAPI application created
[x] Python environment configured
[x] PostgreSQL running
[x] Qdrant running
[x] Environment configuration created
[x] Firebase project configured
[x] Gemini configuration prepared
[x] Backend starts successfully
[x] Frontend starts successfully
[x] /health works
[x] PostgreSQL connection works
[x] Qdrant connection works
[x] Alembic initialized
[x] Basic testing works
[x] README created
[x] .gitignore created
[x] Documentation structure established
47. Phase 9 Architecture

The final development environment will look like:

                    GitHub
                       │
                       ▼
               Career Agent Repo
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
      Angular                    FastAPI
   localhost:4200              localhost:8000
                                    │
                 ┌──────────────────┼──────────────────┐
                 ▼                  ▼                  ▼
             PostgreSQL           Qdrant          Firebase
              :5432              :6333              Auth
                                    │
                                    ▼
                             AI / Agent Layer
                              │           │
                              ▼           ▼
                            Gemini     Hugging Face
48. Important Decision

At this point, we are intentionally not deploying to AWS or another cloud provider.

The first target is:

LOCAL MVP
   ↓
Use it ourselves
   ↓
Validate whether it actually helps job hunting
   ↓
Fix product/workflow problems
   ↓
Only then
   ↓
Production architecture + paid infrastructure

This matches the product strategy: prove that the agent can genuinely improve your own job search before spending money on scale.