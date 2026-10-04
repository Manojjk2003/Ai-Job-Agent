Phase 10.2 — Backend Foundation + PostgreSQL

We’ll now move from the empty FastAPI skeleton to the real backend foundation: configuration, SQLAlchemy, PostgreSQL connection, Alembic migrations, and the first real Candidate model.

This is the foundation every later backend feature will depend on.

10.2.1 Goal

By the end of this phase:

FastAPI
   │
   ├── Config (.env)
   │
   ├── SQLAlchemy
   │       │
   │       ▼
   │   PostgreSQL
   │
   └── Alembic
           │
           ▼
      Database migrations

We will have:

PostgreSQL running through Docker
SQLAlchemy configured
database session management
environment-based configuration
Alembic configured
first database model: Candidate
first migration
migration applied successfully
FastAPI connected to the database
/health still working
10.2.2 Why PostgreSQL?

Our application has highly relational data.

For example:

Candidate
   │
   ├── Candidate Profile
   ├── Role Profiles
   ├── Skills
   ├── Experiences
   ├── Projects
   ├── Resumes
   └── Applications
          │
          └── Jobs
                │
                └── Companies

This is exactly the type of structure PostgreSQL handles well.

We don't want the database to become:

candidate = {
    everything about candidate,
    all jobs,
    all resumes,
    all applications,
    all companies
}

Instead, we want normalized relational tables.

10.2.3 Install Backend Dependencies

Inside:

career-agent/backend

activate your virtual environment.

Windows:

.\.venv\Scripts\activate

Then install:

pip install fastapi uvicorn sqlalchemy psycopg[binary] alembic pydantic pydantic-settings

Verify:

pip list

Important packages:

Package	Purpose
FastAPI	API framework
Uvicorn	Runs FastAPI
SQLAlchemy	ORM/database toolkit
psycopg	PostgreSQL driver
Alembic	Database migrations
Pydantic	Data validation
Pydantic Settings	Environment configuration
10.2.4 Backend Structure

Update the backend to:

backend/
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── health.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── base.py
│       ├── session.py
│       │
│       └── models/
│           ├── __init__.py
│           └── candidate.py
│
├── migrations/
├── alembic.ini
├── pyproject.toml
└── .env

This structure is intentional.

We are separating:

API
Core configuration
Database
Models

Later we will add:

repositories/
services/
providers/
agents/
10.2.5 Environment Configuration

Create:

backend/.env

For local development:

APP_NAME=Career Agent API
APP_ENV=development
DEBUG=true

DATABASE_URL=postgresql+psycopg://career_agent:career_agent_password@localhost:5432/career_agent

Do not commit this file.

Your root .gitignore should contain:

.env
*.env
!.env.example

The repository should only contain:

.env.example

For example:

APP_NAME=Career Agent API
APP_ENV=development
DEBUG=true

DATABASE_URL=postgresql+psycopg://career_agent:career_agent_password@localhost:5432/career_agent
10.2.6 Configuration Class

Create:

backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Career Agent API"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
What is happening?

When we write:

settings.database_url

Pydantic Settings reads:

.env

and gets:

DATABASE_URL=...

So instead of writing this everywhere:

postgresql+psycopg://career_agent:...

we write:

settings.database_url

This is important because production will use a different database.

10.2.7 PostgreSQL Docker Configuration

Your root docker-compose.yml should contain PostgreSQL and Qdrant.

For example:

services:
  postgres:
    image: postgres:16
    container_name: career-agent-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: career_agent
      POSTGRES_PASSWORD: career_agent_password
      POSTGRES_DB: career_agent
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant:latest
    container_name: career-agent-qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  postgres_data:
  qdrant_data:

Start:

docker compose up -d

Check:

docker compose ps

You should see:

career-agent-postgres
career-agent-qdrant
10.2.8 SQLAlchemy Base

Create:

backend/app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

This Base becomes the parent for our SQLAlchemy models.

For example:

class Candidate(Base):
    ...

SQLAlchemy then knows:

This Python class represents a database table.

10.2.9 Database Session

Create:

backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

This is extremely important.

A request might come in:

GET /candidates/123

FastAPI can obtain a database session:

db = get_db()

Use it:

db.query(...)

Then close it:

db.close()

So we don't leave database connections hanging.

10.2.10 First Real Model — Candidate

Create:

backend/app/db/models/candidate.py
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    firebase_uid: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
10.2.11 Understand This Model

The Python class:

Candidate

represents:

candidates

database table.

This:

id

becomes:

id UUID PRIMARY KEY

This:

firebase_uid

connects our application user to Firebase Authentication.

Example:

Firebase
   │
   │ uid
   ▼
Candidate.firebase_uid

We are deliberately not putting Firebase's entire user object into PostgreSQL.

Firebase handles identity.

PostgreSQL handles application data.

10.2.12 Model Registration

Create:

backend/app/db/models/__init__.py
from app.db.models.candidate import Candidate

__all__ = ["Candidate"]

Then update:

backend/app/db/base.py

to:

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.db.models import Candidate  # noqa: E402,F401

The import makes sure Alembic knows about the model.

This is an important concept:

Alembic
   │
   ▼
Base.metadata
   │
   ▼
Candidate table definition
10.2.13 Initialize Alembic

From:

backend/

run:

alembic init migrations

This creates:

migrations/
├── versions/
├── env.py
├── script.py.mako
└── README

and:

alembic.ini
10.2.14 Configure Alembic

Open:

backend/migrations/env.py

Import:

from app.core.config import settings
from app.db.base import Base

Then set:

target_metadata = Base.metadata

And configure the database URL dynamically:

config.set_main_option(
    "sqlalchemy.url",
    settings.database_url,
)

The important idea is:

.env
 ↓
Settings
 ↓
Alembic
 ↓
PostgreSQL

We don't want the database password hardcoded inside alembic.ini.

10.2.15 Create First Migration

Run:

alembic revision --autogenerate -m "create candidates table"

Alembic should detect:

Candidate model

and generate a migration inside:

migrations/versions/

You should see something conceptually like:

create candidates table
10.2.16 Apply Migration

Run:

alembic upgrade head

Now PostgreSQL should contain:

candidates

and Alembic's own:

alembic_version

table.

10.2.17 Verify Database

You can connect to PostgreSQL:

docker exec -it career-agent-postgres psql -U career_agent -d career_agent

Then:

\dt

You should see:

candidates
alembic_version

Then:

\d candidates

You should see fields such as:

id
firebase_uid
full_name
email
created_at
updated_at

Exit:

\q
10.2.18 Why Alembic Instead of create_all()?

You may wonder why we don't simply do:

Base.metadata.create_all(engine)

That can work for tiny experiments.

But our application will eventually have dozens of tables.

For example:

Candidate
CandidateProfile
Experience
ExperienceAchievement
Education
Project
Skill
Job
Company
Application
Resume
...

We need controlled database changes.

Example:

Version 1
candidates
Version 2
candidates
candidate_profiles
Version 3
skills
candidate_skills
Version 4
companies
jobs

Alembic lets us track:

Migration 001
Migration 002
Migration 003
Migration 004

This becomes essential when working on a real application.

10.2.19 Connect FastAPI to Database

Our /health endpoint currently only checks whether FastAPI is alive.

Later we'll have two different concepts:

Application health
        +
Database health
        +
External provider health

For now, keep /health simple.

Don't put database logic directly into main.py.

The application structure should remain:

main.py
   ↓
router
   ↓
endpoint
   ↓
service
   ↓
repository
   ↓
database

This separation will become important as the project grows.

10.2.20 Run FastAPI

From backend:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/docs

You should see Swagger.

And:

GET /health

should return:

{
  "status": "ok"
}
10.2.21 Test Database Connection

Before moving forward, verify:

Docker
docker compose ps
PostgreSQL
running
Migration
alembic current
FastAPI
uvicorn app.main:app --reload
Swagger
http://127.0.0.1:8000/docs
10.2.22 What We Have Built

Our architecture is now becoming real:

                    ┌──────────────┐
                    │   Angular    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    └──────┬───────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
            Configuration       SQLAlchemy
                  │                 │
                  │                 ▼
                  │            PostgreSQL
                  │
                  ▼
                 .env

Alembic
   │
   ▼
Database migrations
   │
   ▼
PostgreSQL schema

This is the first point where the project has a real persistent backend, rather than just an API skeleton.

10.2.23 Very Important Concept for Your Learning

You should understand the difference between these four things:

SQLAlchemy Model

Python representation:

class Candidate(Base):
Database Table

Actual PostgreSQL structure:

CREATE TABLE candidates (...);
Database Session

Connection/context used to perform operations:

db.query(...)
Alembic Migration

Version-controlled database change:

001_create_candidates.py

So:

Python Model
      ↓
SQLAlchemy Metadata
      ↓
Alembic Migration
      ↓
PostgreSQL Table

This flow is something you should be able to explain in an interview.

10.2.24 Phase 10.2 Definition of Done

Don't move to 10.3 until all of these work:

 PostgreSQL running in Docker
 Qdrant running
 .env working
 Pydantic Settings working
 SQLAlchemy installed
 PostgreSQL driver installed
 database engine created
 database session created
 Candidate model created
 Alembic initialized
 Alembic detects Candidate
 migration generated
 migration applied
 candidates table exists
 FastAPI starts
 /health works
 Swagger works
 no secrets committed to Git