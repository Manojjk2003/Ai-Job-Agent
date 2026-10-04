# Phase 10.3 — PostgreSQL + Alembic Integration

Now we’ll make the database layer **proper enough to build on**, instead of just proving that PostgreSQL works.

The main goal is:

```text
FastAPI
   ↓
Dependency
   ↓
SQLAlchemy Session
   ↓
Repository/Service
   ↓
PostgreSQL
```

And:

```text
SQLAlchemy Models
       ↓
     Alembic
       ↓
   Migrations
       ↓
  PostgreSQL Schema
```

## 10.3.1 What we are fixing

In 10.2 we created the pieces individually.

Now we establish the conventions we will use for the entire application:

* one database engine
* one session factory
* request-scoped DB sessions
* centralized model imports
* Alembic using the same configuration
* migration naming/versioning
* database health check
* first DB-backed API test
* proper transaction handling

---

## 10.3.2 Final Database Structure

Keep this:

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   ├── health.py
│   │   └── v1/
│   │
│   ├── core/
│   │   └── config.py
│   │
│   └── db/
│       ├── base.py
│       ├── session.py
│       └── models/
│           ├── __init__.py
│           └── candidate.py
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
└── .env
```

The important architectural rule is:

> **Routes should not directly contain database implementation logic.**

Later:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

---

# 10.3.3 Improve Database Configuration

Update:

```text
backend/app/core/config.py
```

to:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Career Agent API"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
```

### Why `extra="ignore"`?

Suppose later `.env` contains:

```env
GEMINI_API_KEY=...
FIREBASE_PROJECT_ID=...
QDRANT_URL=...
```

Our current Settings class doesn't need all of those yet.

`extra="ignore"` prevents unrelated environment variables from causing configuration errors.

Later, we'll explicitly add the settings we need.

---

# 10.3.4 Improve SQLAlchemy Engine

Update:

```text
backend/app/db/session.py
```

```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

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


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

### Why `pool_pre_ping=True`?

Database connections can become stale.

For example:

```text
Application
    │
    └── connection ──X── PostgreSQL
```

The database may restart.

Without checking the connection, the application could try using a dead connection.

`pool_pre_ping=True` helps SQLAlchemy verify pooled connections before using them.

---

# 10.3.5 Understand `yield`

This is important for your interview preparation.

We have:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

FastAPI sees this as a dependency.

Conceptually:

```text
Request starts
      ↓
create DB session
      ↓
give session to endpoint
      ↓
endpoint finishes
      ↓
close session
```

So:

```python
db = SessionLocal()
```

doesn't mean:

> Keep this connection forever.

It means:

> Create a database session for this request/context.

---

# 10.3.6 Create a Database Health Check

Now we want to distinguish:

```text
API is running
```

from:

```text
API + database are working
```

Update:

```text
backend/app/api/health.py
```

```python
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db


router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "ok",
    }


@router.get("/health/db")
def database_health(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
```

---

# 10.3.7 What Is `Depends()`?

This is one of the FastAPI concepts you should understand deeply.

We write:

```python
db: Session = Depends(get_db)
```

FastAPI effectively handles:

```text
Request
   ↓
get_db()
   ↓
Session
   ↓
endpoint
```

Instead of manually doing:

```python
db = SessionLocal()
```

inside every route.

This is called **dependency injection**.

Later we'll use the same pattern for:

```text
Current user
Database
Authorization
Services
```

For example:

```python
current_user = Depends(get_current_user)
```

This becomes especially important when we implement Firebase Authentication.

---

# 10.3.8 Register Health Router

Make sure your router structure looks like:

```text
app
└── api
    ├── router.py
    └── health.py
```

`health.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/db")
def database_health(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
```

Then:

```text
app/api/router.py
```

```python
from fastapi import APIRouter

from app.api.health import router as health_router


api_router = APIRouter()

api_router.include_router(health_router)
```

And:

```text
app/main.py
```

```python
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(api_router)
```

---

# 10.3.9 Test the Database Health

Start PostgreSQL:

```powershell
docker compose up -d postgres
```

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Run:

```text
GET /health/db
```

Expected:

```json
{
  "status": "ok",
  "database": "connected"
}
```

This proves:

```text
FastAPI
   ↓
Dependency Injection
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

is working.

---

# 10.3.10 Transaction Handling

Now an important concept.

Suppose we later create a candidate:

```python
candidate = Candidate(...)
db.add(candidate)
```

That doesn't necessarily mean the database transaction has been permanently committed.

We need:

```python
db.commit()
```

Conceptually:

```text
db.add()
   ↓
Session contains change
   ↓
db.commit()
   ↓
PostgreSQL permanently stores transaction
```

If something fails:

```python
db.rollback()
```

Conceptually:

```text
Transaction
     │
     ├── operation 1 ✓
     ├── operation 2 ✓
     ├── operation 3 ✗
     │
     ▼
   rollback
     │
     ▼
undo transaction
```

This becomes very important when one operation touches multiple tables.

---

# 10.3.11 Create a Simple Candidate Repository

We're not building the full repository architecture yet, but we'll establish the pattern.

Create:

```text
backend/app/repositories/
```

Then:

```text
backend/app/repositories/candidate_repository.py
```

```python
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.candidate import Candidate


def get_candidate_by_id(
    db: Session,
    candidate_id: uuid.UUID,
) -> Candidate | None:
    statement = select(Candidate).where(
        Candidate.id == candidate_id
    )

    return db.scalar(statement)
```

Notice something important.

We're not doing this in the API:

```python
db.query(Candidate)...
```

Instead:

```text
API
 ↓
Repository
 ↓
SQLAlchemy
```

The API should focus on HTTP behavior.

The repository should focus on database access.

---

# 10.3.12 Why `select()`?

Modern SQLAlchemy supports:

```python
select(Candidate)
```

which represents a SQL query.

Conceptually:

```python
select(Candidate).where(
    Candidate.id == candidate_id
)
```

becomes something like:

```sql
SELECT *
FROM candidates
WHERE id = ...;
```

You don't need to memorize SQLAlchemy syntax yet.

You need to understand:

```text
Python query expression
        ↓
SQLAlchemy
        ↓
SQL
        ↓
PostgreSQL
```

---

# 10.3.13 Candidate Creation

Create:

```text
backend/app/repositories/candidate_repository.py
```

with:

```python
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.candidate import Candidate


def get_candidate_by_id(
    db: Session,
    candidate_id: uuid.UUID,
) -> Candidate | None:
    statement = select(Candidate).where(
        Candidate.id == candidate_id
    )

    return db.scalar(statement)


def get_candidate_by_firebase_uid(
    db: Session,
    firebase_uid: str,
) -> Candidate | None:
    statement = select(Candidate).where(
        Candidate.firebase_uid == firebase_uid
    )

    return db.scalar(statement)


def create_candidate(
    db: Session,
    firebase_uid: str,
    full_name: str | None = None,
    email: str | None = None,
) -> Candidate:
    candidate = Candidate(
        firebase_uid=firebase_uid,
        full_name=full_name,
        email=email,
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate
```

The flow is:

```text
create_candidate()
       ↓
Candidate(...)
       ↓
db.add()
       ↓
db.commit()
       ↓
db.refresh()
       ↓
return candidate
```

---

# 10.3.14 Why `refresh()`?

After:

```python
db.commit()
```

PostgreSQL may have generated/confirmed values.

For example:

```text
id
created_at
updated_at
```

`refresh()` tells SQLAlchemy:

> Reload the object's current database state.

So:

```python
db.refresh(candidate)
```

ensures the Python object represents the persisted database record.

---

# 10.3.15 Migration Verification

Now check:

```powershell
alembic current
```

Then:

```powershell
alembic history
```

You should see your migration.

For example:

```text
<revision> -> create candidates table
```

Then:

```powershell
alembic upgrade head
```

If you're already at `head`, Alembic should report that there is nothing to upgrade.

---

# 10.3.16 Important Migration Rule

From now on:

### Never manually modify PostgreSQL tables for application schema changes.

If we add:

```text
Candidate.phone
```

don't manually execute:

```sql
ALTER TABLE candidates ...
```

Instead:

1. modify SQLAlchemy model
2. generate migration
3. inspect migration
4. apply migration

Flow:

```text
Model changed
     ↓
alembic revision --autogenerate
     ↓
Inspect migration
     ↓
alembic upgrade head
     ↓
PostgreSQL updated
```

This gives us reproducible environments.

---

# 10.3.17 Test Migration Reproducibility

This is a useful real-world test.

You can completely recreate the PostgreSQL container/database if needed:

```powershell
docker compose down -v
```

⚠️ This deletes the Docker volumes, so only do this with local development data you don't need.

Then:

```powershell
docker compose up -d postgres
```

And:

```powershell
alembic upgrade head
```

The database should be recreated entirely from migrations.

That's one of the reasons migrations matter.

---

# 10.3.18 What You Should Be Able to Explain

For your interview preparation, make sure you can answer:

### Q1. Why PostgreSQL?

Because our application has strongly relational entities such as candidates, jobs, companies, resumes and applications, with relationships, constraints and transactional requirements.

### Q2. What is SQLAlchemy?

A Python SQL toolkit/ORM that allows us to work with relational databases using Python objects and expressions while still interacting with SQL databases.

### Q3. What is a database session?

A SQLAlchemy session manages database operations and transaction state for a unit of work.

### Q4. Why use dependency injection for DB sessions?

It provides a controlled session lifecycle and avoids manually creating/closing sessions in every endpoint.

### Q5. What is Alembic?

A database migration tool used to version and apply schema changes.

### Q6. Why not `create_all()`?

Because production applications need controlled, versioned schema changes that can be applied consistently across environments.

### Q7. What does `commit()` do?

It commits the current transaction so changes become persistent in the database.

### Q8. What does `rollback()` do?

It reverses uncommitted changes in the current transaction.

---

# 10.3.19 Current Architecture

We have now reached:

```text
                    Angular
                       │
                       ▼
                    FastAPI
                       │
                 ┌─────┴─────┐
                 │           │
              Router       Depends
                 │           │
                 │       DB Session
                 │           │
                 ▼           ▼
              Service     SQLAlchemy
                              │
                              ▼
                         PostgreSQL
                              ▲
                              │
                           Alembic
                              │
                         Migrations
```

And later:

```text
FastAPI
   │
   ├── Services
   ├── Repositories
   ├── Providers
   ├── Agents
   └── Background Jobs
```

This is the foundation we wanted before adding actual business functionality.

---

# 10.3.20 Definition of Done

Before moving on:

* [ ] PostgreSQL works through Docker
* [ ] SQLAlchemy engine works
* [ ] session factory works
* [ ] FastAPI dependency injection works
* [ ] `/health/db` works
* [ ] Candidate model exists
* [ ] Candidate migration exists
* [ ] `alembic upgrade head` works
* [ ] repository pattern established
* [ ] candidate lookup repository works
* [ ] candidate creation repository works
* [ ] transaction concepts understood
* [ ] migration can recreate the schema

---

## Next: Phase 10.4 — Firebase Authentication

This is where the project starts becoming a **real user application**.

We'll implement:

```text
User logs in with Firebase
        ↓
Firebase gives ID token
        ↓
Angular sends token
        ↓
FastAPI verifies token
        ↓
Firebase UID
        ↓
Candidate.firebase_uid
        ↓
Candidate record
```

Then we can establish the critical security rule:

> **A candidate can only access their own career data.**
