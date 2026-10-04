# Phase 10.5 — Candidate Onboarding

Now we build the **first real user-facing career flow**.

The goal is not just to collect a name and email. We need to create the **source-of-truth candidate profile** that every later agent depends on.

```text
Firebase Login
      ↓
Candidate
      ↓
Onboarding
      ↓
Candidate Profile
      ↓
Preferences
      ↓
Role Profiles
      ↓
Matching / Resume / Job Discovery
```

The most important rule:

> **We collect facts from the candidate. We do not let the AI invent candidate information.**

---

# 10.5.1 What Are We Building?

After signup, the user should be able to provide:

```text
Basic Information
├── Full name
├── Email
├── Phone
├── Current location
└── LinkedIn / GitHub

Professional Information
├── Current designation
├── Years of experience
├── Career status
└── Notice period

Education
├── Degree
├── College
├── Graduation year
└── CGPA

Job Preferences
├── Desired roles
├── Preferred locations
├── Remote / Hybrid / On-site
├── Salary expectations
└── Job type
```

But we're going to build this incrementally.

---

# 10.5.2 Why Separate Candidate and Candidate Profile?

We already have:

```text
candidates
```

That table represents the **application identity**.

Now we'll create:

```text
candidate_profiles
```

which represents professional information.

Conceptually:

```text
Candidate
│
├── Authentication identity
│
└── Candidate Profile
       ├── Professional information
       ├── Location
       ├── Summary
       ├── Experience
       ├── Education
       └── Preferences
```

This separation is useful because authentication identity and career information have different responsibilities.

---

# 10.5.3 Database Design

Create:

```text
candidate_profiles
```

with:

```text
id
candidate_id
phone
location
headline
summary
years_experience
current_designation
linkedin_url
github_url
created_at
updated_at
```

Relationship:

```text
candidates
    1
    │
    │
    1
    ▼
candidate_profiles
```

For the MVP, we'll use **one profile per candidate**.

---

# 10.5.4 SQLAlchemy Model

Create:

```text
backend/app/db/models/candidate_profile.py
```

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    headline: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    years_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    current_designation: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    linkedin_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    github_url: Mapped[str | None] = mapped_column(
        String(500),
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
```

---

# 10.5.5 Important Improvement: Foreign Key

The model should actually enforce:

```text
candidate_profiles.candidate_id
        ↓
candidates.id
```

So update the import:

```python
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
```

and:

```python
candidate_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("candidates.id", ondelete="CASCADE"),
    unique=True,
    nullable=False,
    index=True,
)
```

Now PostgreSQL itself understands the relationship.

This is much better than relying only on application code.

---

# 10.5.6 Register the Model

Update:

```text
backend/app/db/models/__init__.py
```

```python
from app.db.models.candidate import Candidate
from app.db.models.candidate_profile import CandidateProfile

__all__ = [
    "Candidate",
    "CandidateProfile",
]
```

Because `base.py` imports the models:

```python
from app.db.models import Candidate
```

change it to:

```python
from app.db.models import Candidate, CandidateProfile
```

---

# 10.5.7 Create Migration

From:

```text
backend/
```

run:

```powershell
alembic revision --autogenerate -m "create candidate profiles"
```

Inspect the generated migration.

It should contain creation of:

```text
candidate_profiles
```

and the foreign key:

```text
candidate_profiles.candidate_id
        ↓
candidates.id
```

Then:

```powershell
alembic upgrade head
```

Verify:

```powershell
alembic current
```

---

# 10.5.8 Why Foreign Keys Matter

Suppose someone accidentally tries to create:

```text
candidate_profile
candidate_id = "does-not-exist"
```

Without a foreign key, PostgreSQL might accept it.

With:

```text
FOREIGN KEY(candidate_id)
REFERENCES candidates(id)
```

the database rejects it.

So validation exists at multiple levels:

```text
Frontend validation
        ↓
Pydantic validation
        ↓
Service/business rules
        ↓
Database constraints
```

We don't rely on only one layer.

---

# 10.5.9 Create Pydantic Schemas

Now separate:

```text
Database models
```

from:

```text
API request/response models
```

Create:

```text
backend/app/schemas/
```

Then:

```text
backend/app/schemas/candidate_profile.py
```

```python
import uuid

from pydantic import BaseModel, Field, HttpUrl


class CandidateProfileCreate(BaseModel):
    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    location: str | None = Field(
        default=None,
        max_length=255,
    )

    headline: str | None = Field(
        default=None,
        max_length=255,
    )

    summary: str | None = None

    years_experience: int | None = Field(
        default=None,
        ge=0,
    )

    current_designation: str | None = Field(
        default=None,
        max_length=255,
    )

    linkedin_url: HttpUrl | None = None

    github_url: HttpUrl | None = None


class CandidateProfileResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID

    phone: str | None
    location: str | None
    headline: str | None
    summary: str | None
    years_experience: int | None
    current_designation: str | None
    linkedin_url: str | None
    github_url: str | None

    model_config = {
        "from_attributes": True,
    }
```

---

# 10.5.10 Why Do We Need Pydantic Schemas?

Don't expose SQLAlchemy models directly from APIs.

Think:

```text
SQLAlchemy Model
      ↓
Database representation
```

while:

```text
Pydantic Schema
      ↓
API contract
```

For example, the user may send:

```json
{
  "years_experience": -10
}
```

Pydantic rejects it because:

```python
ge=0
```

is enforced.

This protects the application before the data reaches PostgreSQL.

---

# 10.5.11 Repository

Create:

```text
backend/app/repositories/candidate_profile_repository.py
```

```python
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.candidate_profile import CandidateProfile


def get_profile_by_candidate_id(
    db: Session,
    candidate_id: uuid.UUID,
) -> CandidateProfile | None:
    statement = select(CandidateProfile).where(
        CandidateProfile.candidate_id == candidate_id
    )

    return db.scalar(statement)


def create_profile(
    db: Session,
    candidate_id: uuid.UUID,
    data: dict,
) -> CandidateProfile:
    profile = CandidateProfile(
        candidate_id=candidate_id,
        **data,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def update_profile(
    db: Session,
    profile: CandidateProfile,
    data: dict,
) -> CandidateProfile:
    for field, value in data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile
```

---

# 10.5.12 Service Layer

Create:

```text
backend/app/services/candidate_profile_service.py
```

```python
import uuid

from sqlalchemy.orm import Session

from app.repositories.candidate_profile_repository import (
    create_profile,
    get_profile_by_candidate_id,
    update_profile,
)


def get_candidate_profile(
    db: Session,
    candidate_id: uuid.UUID,
):
    return get_profile_by_candidate_id(
        db,
        candidate_id,
    )


def create_candidate_profile(
    db: Session,
    candidate_id: uuid.UUID,
    data: dict,
):
    existing = get_profile_by_candidate_id(
        db,
        candidate_id,
    )

    if existing:
        return existing

    return create_profile(
        db,
        candidate_id,
        data,
    )


def update_candidate_profile(
    db: Session,
    candidate_id: uuid.UUID,
    data: dict,
):
    profile = get_profile_by_candidate_id(
        db,
        candidate_id,
    )

    if not profile:
        return create_profile(
            db,
            candidate_id,
            data,
        )

    return update_profile(
        db,
        profile,
        data,
    )
```

---

# 10.5.13 One Important Problem

How do we get:

```text
candidate_id
```

?

We don't ask the frontend to send it.

Remember:

```text
Firebase Token
       ↓
Firebase UID
       ↓
Candidate
       ↓
candidate.id
```

So create a reusable service that gets the candidate from the authenticated user.

Create:

```text
backend/app/services/current_candidate_service.py
```

```python
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.candidate_repository import (
    get_candidate_by_firebase_uid,
)


def get_current_candidate(
    db: Session,
    firebase_uid: str,
):
    candidate = get_candidate_by_firebase_uid(
        db,
        firebase_uid,
    )

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return candidate
```

This gives us:

```text
Verified Firebase UID
        ↓
Candidate
        ↓
Candidate ID
```

---

# 10.5.14 Profile API

Create:

```text
backend/app/api/v1/profiles.py
```

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.candidate_profile import (
    CandidateProfileCreate,
    CandidateProfileResponse,
)
from app.services.candidate_profile_service import (
    create_candidate_profile,
    get_candidate_profile,
    update_candidate_profile,
)
from app.services.current_candidate_service import (
    get_current_candidate,
)


router = APIRouter(
    prefix="/profile",
    tags=["Candidate Profile"],
)


@router.get(
    "",
    response_model=CandidateProfileResponse | None,
)
def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    candidate = get_current_candidate(
        db,
        current_user["uid"],
    )

    return get_candidate_profile(
        db,
        candidate.id,
    )


@router.post(
    "",
    response_model=CandidateProfileResponse,
)
def create_my_profile(
    payload: CandidateProfileCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    candidate = get_current_candidate(
        db,
        current_user["uid"],
    )

    profile = create_candidate_profile(
        db=db,
        candidate_id=candidate.id,
        data=payload.model_dump(
            mode="json",
        ),
    )

    return profile
```

---

# 10.5.15 Update Router

In:

```text
backend/app/api/v1/router.py
```

add:

```python
from app.api.v1.candidates import router as candidates_router
from app.api.v1.profiles import router as profiles_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(candidates_router)
api_router.include_router(profiles_router)
```

Now:

```text
GET  /api/v1/profile
POST /api/v1/profile
```

---

# 10.5.16 Our First Real Onboarding Flow

The flow now becomes:

```text
User logs in
     ↓
Firebase
     ↓
ID token
     ↓
FastAPI
     ↓
get_current_user()
     ↓
Firebase UID
     ↓
Candidate
     ↓
Candidate Profile
     ↓
PostgreSQL
```

The browser never needs to send:

```text
candidate_id
```

That's an important security property.

---

# 10.5.17 What Should the Frontend Send?

Example:

```json
{
  "phone": "+91XXXXXXXXXX",
  "location": "Bangalore",
  "headline": "Junior Software Engineer",
  "summary": "Software engineer with experience building web applications...",
  "years_experience": 1,
  "current_designation": "Junior Software Engineer",
  "linkedin_url": "https://linkedin.com/in/example",
  "github_url": "https://github.com/example"
}
```

The backend determines the candidate from the authentication token.

---

# 10.5.18 Don't Let AI Generate the Source of Truth

This is particularly important for our product.

We will eventually use AI to:

* summarize experience
* tailor resumes
* analyze JDs
* identify matching skills
* suggest improvements

But the source-of-truth profile should be:

```text
Candidate-provided facts
        ↓
Validated
        ↓
Stored
```

Not:

```text
LLM
 ↓
Invented candidate profile
```

For example, if the candidate says:

```text
Angular
FastAPI
MySQL
Docker
```

the AI can reframe those facts for a specific JD.

It cannot decide:

```text
Candidate knows Kubernetes
```

unless we have evidence.

This protects against resume fabrication.

---

# 10.5.19 Onboarding vs Resume Parsing

Later we will allow:

```text
Upload resume
      ↓
Parse resume
      ↓
Extract candidate information
      ↓
Show extracted information
      ↓
Candidate confirms/edits
      ↓
Save to profile
```

Important:

> Parsed resume information should **not automatically become trusted truth** without user confirmation.

Our eventual flow:

```text
Resume
  ↓
Parser
  ↓
AI extraction
  ↓
Candidate review
  ↓
Confirmed facts
  ↓
Candidate Profile
```

This is much safer.

---

# 10.5.20 Frontend Onboarding Comes Next

For now, backend is enough to establish the contract.

The Angular flow will eventually be:

```text
/login
   ↓
/onboarding
   ↓
/profile
   ↓
/dashboard
```

The onboarding form will call:

```http
POST /api/v1/profile
```

with:

```http
Authorization: Bearer <firebase-id-token>
```

---

# 10.5.21 Testing

Create:

```text
backend/tests/
├── unit/
├── integration/
└── api/
```

We'll progressively add tests.

For this phase, verify manually first:

### 1. Login

Firebase authentication works.

### 2. Authenticated candidate

```http
GET /api/v1/candidates/me
```

returns the current candidate.

### 3. Create profile

```http
POST /api/v1/profile
```

creates:

```text
candidate_profiles
```

### 4. Get profile

```http
GET /api/v1/profile
```

returns the saved profile.

### 5. Unauthorized request

Calling:

```http
GET /api/v1/profile
```

without a Firebase token returns:

```text
401
```

### 6. Ownership

Candidate A's token must never retrieve Candidate B's profile.

---

# 10.5.22 Database Now Looks Like

```text
┌─────────────────────────┐
│       candidates        │
├─────────────────────────┤
│ id PK                   │
│ firebase_uid UNIQUE     │
│ full_name               │
│ email                   │
│ created_at              │
│ updated_at              │
└────────────┬────────────┘
             │
             │ 1:1
             ▼
┌─────────────────────────┐
│   candidate_profiles    │
├─────────────────────────┤
│ id PK                   │
│ candidate_id FK UNIQUE  │
│ phone                   │
│ location                │
│ headline                │
│ summary                 │
│ years_experience        │
│ current_designation     │
│ linkedin_url            │
│ github_url              │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
```

This is the beginning of our candidate domain.

---

# 10.5.23 What You Should Understand

You should now be able to explain this complete request:

> A user logs into Firebase from Angular. Firebase returns an ID token. Angular sends that token to FastAPI as a Bearer token. FastAPI verifies the token through Firebase Admin SDK, obtains the Firebase UID, finds the corresponding Candidate record, and uses the
