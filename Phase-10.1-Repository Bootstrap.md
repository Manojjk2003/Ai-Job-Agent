Phase 10.1 — Repository Bootstrap

This is the first actual implementation step. We are going to turn the architecture into a real repository, but we will keep the scope deliberately small.

1. Objective

At the end of Phase 10.1, we should have:

career-agent/
│
├── frontend/
│
├── backend/
│
├── docs/
│
├── infrastructure/
│
├── scripts/
│
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md

And the following should work:

Angular        → localhost:4200
FastAPI        → localhost:8000
PostgreSQL     → localhost:5432
Qdrant         → localhost:6333
Git            → initialized

We are not implementing authentication, agents, jobs, resumes, or AI yet.

2. Prerequisites

Before starting, verify:

Node.js
npm
Angular CLI
Python
pip
Git
Docker
Docker Compose

Check:

node --version
npm --version
ng version
python --version
pip --version
git --version
docker --version
docker compose version

The exact versions should be selected based on the currently supported stable versions you have installed rather than blindly forcing a particular version.

3. Create the Repository

Create the root directory:

mkdir career-agent
cd career-agent

Initialize Git:

git init

Expected:

Initialized empty Git repository
4. Create Root Directories

Create:

frontend/
backend/
docs/
infrastructure/
scripts/
tests/

The repository now becomes:

career-agent/
├── frontend/
├── backend/
├── docs/
├── infrastructure/
├── scripts/
└── tests/
5. Why We Don't Create Everything Yet

You may notice that the Phase 4 architecture contains many folders:

repositories/
services/
providers/
agents/
vector/
...

We should not immediately create every file.

Why?

Because empty architecture creates the illusion that functionality exists.

Instead:

Need feature
   ↓
Create required layer
   ↓
Implement
   ↓
Test

This keeps the repository clean.

6. Create Angular Application

From:

career-agent/frontend/

create the Angular application.

Conceptually:

ng new career-agent-ui

Use the Angular setup appropriate for the current Angular CLI.

The application should use:

TypeScript
Standalone APIs
Routing

Avoid creating an old-style AppModule architecture.

7. Why Standalone Angular

Our frontend architecture is based on modern Angular.

Instead of:

AppModule
 ├── Components
 ├── Services
 └── Modules

we use:

Application
 ├── Routes
 ├── Components
 ├── Providers
 └── Features

This matches the architecture we want for the project.

8. Initial Angular Structure

After creation:

frontend/
└── career-agent-ui/
    ├── src/
    │   ├── app/
    │   ├── assets/
    │   ├── index.html
    │   ├── main.ts
    │   └── styles.css
    │
    ├── angular.json
    ├── package.json
    └── tsconfig.json

Do not immediately create all feature directories.

9. Run Angular

From:

frontend/career-agent-ui/

run:

npm install
npm start

Then open:

http://localhost:4200

Expected:

Angular application loads successfully.
10. First Verification

At this point:

Browser
   ↓
Angular Dev Server
   ↓
Application loads

Nothing is connected to FastAPI yet.

That is intentional.

11. Create Backend

From:

career-agent/backend/

create the Python environment.

Windows:

python -m venv .venv

Activate:

.venv\Scripts\activate

You should see something similar to:

(.venv)

in your terminal.

12. Backend Dependencies

Initially install only the foundation:

pip install fastapi uvicorn pydantic pydantic-settings

Database dependencies can be added in the next implementation step.

Don't install the entire AI stack yet.

13. Initial FastAPI Structure

Create:

backend/
└── app/
    ├── __init__.py
    ├── main.py
    │
    └── api/
        ├── __init__.py
        └── health.py
14. main.py

The initial application should be intentionally simple:

from fastapi import FastAPI

app = FastAPI(
    title="Career Agent API",
    version="0.1.0",
)

Then register the health endpoint.

The first goal is not architecture complexity.

The first goal is:

Can FastAPI start?

15. Health Endpoint

Create:

GET /health

Response:

{
  "status": "ok"
}

Run:

uvicorn app.main:app --reload
16. Verify FastAPI

Open:

http://localhost:8000/health

Expected:

{
  "status": "ok"
}

Also check:

http://localhost:8000/docs

FastAPI should show its Swagger UI.

This is our first API verification.

17. Understand What Just Happened

The request flow is:

Browser
   │
   │ GET /health
   ▼
Uvicorn
   │
   ▼
FastAPI application
   │
   ▼
Health route
   │
   ▼
JSON response
Uvicorn

Uvicorn is the ASGI server.

It receives HTTP requests and runs the FastAPI application.

FastAPI

FastAPI defines the application and routes.

Route

The /health endpoint defines what happens when that URL is requested.

18. Why main.py Should Stay Small

Don't put:

database logic
authentication
AI
business logic
job search
resume processing

inside main.py.

Eventually:

main.py
   ↓
API Router
   ↓
Service
   ↓
Repository

This follows the architecture we already designed.

19. Create Root .gitignore

At repository root:

.gitignore

Initial contents should cover:

.env
.env.*
!.env.example

.venv/
__pycache__/
*.pyc

node_modules/
dist/
.angular/

.pytest_cache/
.coverage

*.log

.idea/
.vscode/

Do not commit:

.env
.venv
node_modules
20. Create .env.example

At root:

.env.example

Initial structure:

ENVIRONMENT=development

DATABASE_URL=

FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=

GEMINI_API_KEY=

QDRANT_URL=http://localhost:6333

OBJECT_STORAGE_BUCKET=

LOG_LEVEL=INFO

This is documentation, not a secret store.

21. Create docker-compose.yml

Initially we only need infrastructure services:

PostgreSQL
Qdrant

Conceptually:

services:

  postgres:
    image: postgres
    ports:
      - "5432:5432"

  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"

The exact image tags and credentials should be pinned in the actual implementation rather than using unpinned latest tags.

22. PostgreSQL Configuration

Use environment variables for:

POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD

Example local database:

Database:
career_agent

Don't use a real production password in the repository.

For local development, a development-only credential is acceptable.

23. Start PostgreSQL and Qdrant

From repository root:

docker compose up -d

Then:

docker compose ps

Expected conceptually:

postgres    running
qdrant      running
24. PostgreSQL Verification

The first verification is simply:

PostgreSQL container
        ↓
Running
        ↓
Port 5432 available

We will create the actual SQLAlchemy connection in Phase 10.2.

25. Qdrant Verification

Similarly:

Qdrant container
        ↓
Running
        ↓
Port 6333 available

We won't create collections yet.

That belongs to the RAG implementation step.

26. Initial Repository

At this point:

career-agent/
│
├── frontend/
│   └── career-agent-ui/
│
├── backend/
│   ├── .venv/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       └── api/
│           ├── __init__.py
│           └── health.py
│
├── docs/
├── infrastructure/
├── scripts/
├── tests/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
27. Root README

The README should initially explain:

# Career Agent

AI-powered job discovery and application assistant.

## Architecture

Angular
FastAPI
PostgreSQL
Qdrant
Firebase Authentication
Gemini
Google ADK

## Local Development

Frontend:
...

Backend:
...

Infrastructure:
...

Don't write a huge README yet.

It will grow as the project grows.

28. First Git Commit

Once:

Angular works
FastAPI works
Docker works

commit the bootstrap.

Example:

git add .
git commit -m "chore: bootstrap career agent repository"
29. What This Commit Represents

This commit should not contain:

❌ Candidate model
❌ Job model
❌ AI agent
❌ Resume parser
❌ Matching
❌ Authentication

It represents only:

The development environment exists and can run.

30. Phase 10.1 Definition of Done

Before moving forward, verify:

[ ] Git initialized
[ ] Angular project created
[ ] Angular starts
[ ] FastAPI project created
[ ] FastAPI starts
[ ] /health returns 200
[ ] Swagger works
[ ] Docker Compose works
[ ] PostgreSQL container runs
[ ] Qdrant container runs
[ ] .gitignore created
[ ] .env.example created
[ ] README created
[ ] Initial commit created
31. Important: Don't Skip Verification

We should not move to the database model just because the files exist.

The actual test is:

Terminal 1
Angular
   ↓
localhost:4200
   ↓
WORKS

Terminal 2
FastAPI
   ↓
localhost:8000/health
   ↓
WORKS

Terminal 3
Docker
   ↓
PostgreSQL + Qdrant
   ↓
WORKS

Only then:

Phase 10.1 ✅
32. What We Build Next

Once this bootstrap is working, the next implementation step is:

Phase 10.2 — Backend Foundation + PostgreSQL

We will build the actual backend foundation:

FastAPI
   ↓
Configuration
   ↓
Database Session
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
Alembic