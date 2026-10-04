# Phase 10.4 — Firebase Authentication

Now we connect **real user authentication** to the backend.

Until now, anyone who could call our API could potentially access an endpoint. We need to establish the identity boundary:

```text
Angular
   │
   │ Firebase Login
   ▼
Firebase Authentication
   │
   │ ID Token
   ▼
Angular
   │
   │ Authorization: Bearer <token>
   ▼
FastAPI
   │
   │ Verify token
   ▼
Firebase Admin SDK
   │
   │ Firebase UID
   ▼
Candidate
   │
   ▼
PostgreSQL
```

This is a very important phase because **authentication is not just a login screen**. It is what allows our backend to know *who is making the request*.

---

# 10.4.1 Authentication vs Authorization

Understand this distinction first.

### Authentication

> Who are you?

Example:

```text
Firebase UID:
abc123xyz
```

### Authorization

> What are you allowed to access?

Example:

```text
Candidate A
    ↓
Can access Candidate A's profile

Candidate B
    ↓
Cannot access Candidate A's profile
```

So:

```text
Authentication
       ↓
Identity
       ↓
Authorization
       ↓
Access control
```

We'll implement authentication first, then enforce ownership.

---

# 10.4.2 Why Firebase Authentication?

We're already using Firebase Authentication in the architecture.

Firebase handles:

* email/password
* Google login
* authentication lifecycle
* token issuance
* password handling
* identity management

Our FastAPI backend should **not** store passwords.

Instead:

```text
Firebase
    = Identity provider

PostgreSQL
    = Application data
```

That separation is intentional.

---

# 10.4.3 Firebase Architecture

The final flow will be:

```text
┌──────────────┐
│   Angular    │
└──────┬───────┘
       │
       │ Login
       ▼
┌──────────────┐
│   Firebase   │
│     Auth     │
└──────┬───────┘
       │
       │ ID Token
       ▼
┌──────────────┐
│   Angular    │
└──────┬───────┘
       │
       │ Bearer Token
       ▼
┌──────────────┐
│   FastAPI    │
└──────┬───────┘
       │
       │ Verify
       ▼
┌──────────────┐
│ Firebase     │
│ Admin SDK    │
└──────┬───────┘
       │
       │ UID
       ▼
┌──────────────┐
│ PostgreSQL   │
│ Candidate    │
└──────────────┘
```

---

# 10.4.4 Install Firebase Admin SDK

Inside:

```text
career-agent/backend
```

activate your virtual environment.

Install:

```powershell
pip install firebase-admin
```

Verify:

```powershell
pip show firebase-admin
```

---

# 10.4.5 Firebase Client vs Firebase Admin

There are two different Firebase SDK responsibilities.

### Angular

Uses:

```text
Firebase Web SDK
```

Purpose:

```text
Login
Logout
Token management
```

### FastAPI

Uses:

```text
Firebase Admin SDK
```

Purpose:

```text
Verify ID tokens
Read trusted Firebase identity information
```

Do **not** put Firebase Admin credentials in Angular.

The browser is not trusted.

---

# 10.4.6 Firebase Project

Use your Firebase project for this application.

In Firebase Console:

```text
Authentication
    ↓
Sign-in method
```

Enable at least:

```text
Email/Password
```

You can add Google authentication later.

For the MVP, email/password is enough to prove the architecture.

---

# 10.4.7 Backend Firebase Configuration

Create:

```text
backend/app/core/firebase.py
```

For local development, Firebase Admin needs service-account credentials.

The important security rule:

```text
service-account JSON
        ↓
NEVER commit to Git
NEVER put in Angular
NEVER expose through API
```

Add to `.gitignore`:

```gitignore
firebase-service-account.json
*.service-account.json
```

---

# 10.4.8 Recommended Local Configuration

For local development, keep the service account outside the repository when possible.

For example:

```text
C:\Users\<you>\.career-agent\firebase-service-account.json
```

Then configure:

```env
FIREBASE_CREDENTIALS_PATH=C:\Users\<you>\.career-agent\firebase-service-account.json
```

Do **not** put the actual credential into:

```text
.env.example
```

Only document the variable:

```env
FIREBASE_CREDENTIALS_PATH=
```

---

# 10.4.9 Add Firebase Settings

Update:

```text
backend/app/core/config.py
```

Add:

```python
firebase_credentials_path: str
```

So:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Career Agent API"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    firebase_credentials_path: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
```

Then:

```env
FIREBASE_CREDENTIALS_PATH=C:\Users\<you>\.career-agent\firebase-service-account.json
```

---

# 10.4.10 Initialize Firebase Admin

Create:

```text
backend/app/core/firebase.py
```

```python
import firebase_admin
from firebase_admin import credentials

from app.core.config import settings


def initialize_firebase() -> None:
    if firebase_admin._apps:
        return

    credential = credentials.Certificate(
        settings.firebase_credentials_path
    )

    firebase_admin.initialize_app(credential)
```

The important part:

```python
if firebase_admin._apps:
    return
```

prevents initializing the Firebase Admin SDK multiple times during development reloads.

---

# 10.4.11 Initialize During Application Startup

Update:

```text
backend/app/main.py
```

```python
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.firebase import initialize_firebase


initialize_firebase()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(api_router)
```

Now when FastAPI starts:

```text
FastAPI startup
      ↓
initialize_firebase()
      ↓
Firebase Admin SDK ready
```

---

# 10.4.12 Verify Token

Create:

```text
backend/app/core/security.py
```

```python
from fastapi import HTTPException, status
from firebase_admin import auth


def verify_firebase_token(token: str) -> dict:
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc
```

The Firebase Admin SDK verifies:

* signature
* token validity
* expiration
* Firebase-issued identity

We don't manually decode JWTs and assume they're trustworthy.

---

# 10.4.13 Bearer Token

The browser will send:

```http
Authorization: Bearer eyJhbGciOi...
```

The backend needs to extract:

```text
eyJhbGciOi...
```

FastAPI has a convenient security utility for this.

Update `security.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
) -> dict:
    try:
        decoded_token = auth.verify_id_token(
            credentials.credentials
        )

        return decoded_token

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from exc
```

Now we have a reusable dependency:

```python
Depends(get_current_user)
```

---

# 10.4.14 What Does `get_current_user()` Return?

Firebase gives us decoded token information.

Conceptually:

```python
{
    "uid": "abc123",
    "email": "user@example.com",
    "email_verified": True,
    ...
}
```

The most important field for our application is:

```text
uid
```

That maps to:

```text
Candidate.firebase_uid
```

---

# 10.4.15 Create an Authenticated Endpoint

Add to:

```text
backend/app/api/health.py
```

```python
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import get_current_user
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


@router.get("/health/auth")
def authentication_health(
    current_user: dict = Depends(get_current_user),
):
    return {
        "status": "ok",
        "uid": current_user["uid"],
    }
```

Now:

```text
GET /health/auth
```

requires authentication.

Without a token:

```text
401 Unauthorized
```

With a valid Firebase token:

```json
{
  "status": "ok",
  "uid": "firebase-user-id"
}
```

---

# 10.4.16 Why This Is Better Than Sending `user_id`

A dangerous API design would be:

```http
GET /candidates/ABC123
```

and simply trust:

```text
ABC123
```

from the client.

A malicious user could try:

```http
GET /candidates/SOMEONE_ELSES_ID
```

Instead, we establish identity from the verified Firebase token:

```text
Token
 ↓
Firebase UID
 ↓
Candidate
```

Then authorization decides whether the requested resource belongs to that candidate.

---

# 10.4.17 Connect Firebase UID to Candidate

We already have:

```text
candidates.firebase_uid
```

Now create a candidate service.

Create:

```text
backend/app/services/
backend/app/services/candidate_service.py
```

```python
from sqlalchemy.orm import Session

from app.repositories.candidate_repository import (
    create_candidate,
    get_candidate_by_firebase_uid,
)


def get_or_create_candidate(
    db: Session,
    firebase_uid: str,
    email: str | None = None,
    full_name: str | None = None,
):
    candidate = get_candidate_by_firebase_uid(
        db,
        firebase_uid,
    )

    if candidate:
        return candidate

    return create_candidate(
        db=db,
        firebase_uid=firebase_uid,
        email=email,
        full_name=full_name,
    )
```

Now the architecture is:

```text
Firebase UID
     ↓
Candidate Service
     ↓
Candidate Repository
     ↓
PostgreSQL
```

---

# 10.4.18 Create Current Candidate Endpoint

Create:

```text
backend/app/api/v1/candidates.py
```

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.services.candidate_service import get_or_create_candidate


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"],
)


@router.get("/me")
def get_my_candidate(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    candidate = get_or_create_candidate(
        db=db,
        firebase_uid=current_user["uid"],
        email=current_user.get("email"),
    )

    return {
        "id": str(candidate.id),
        "firebase_uid": candidate.firebase_uid,
        "email": candidate.email,
        "full_name": candidate.full_name,
    }
```

This is an important endpoint.

The client doesn't need to say:

```text
"I am candidate 123."
```

It says:

```http
GET /candidates/me
Authorization: Bearer <firebase-token>
```

The backend determines who `"me"` is.

---

# 10.4.19 Register Version 1 Router

Update:

```text
backend/app/api/v1/router.py
```

```python
from fastapi import APIRouter

from app.api.v1.candidates import router as candidates_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(candidates_router)
```

Then update:

```text
backend/app/api/router.py
```

```python
from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.v1.router import api_router as v1_router


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(v1_router)
```

Now our URL is:

```text
GET /api/v1/candidates/me
```

---

# 10.4.20 Full Request Flow

This is one of the most important flows in the entire application.

```text
                    USER
                     │
                     ▼
              ┌────────────┐
              │  Angular   │
              └─────┬──────┘
                    │
                    │ Login
                    ▼
             ┌──────────────┐
             │   Firebase   │
             │     Auth     │
             └──────┬───────┘
                    │
                    │ ID Token
                    ▼
             ┌──────────────┐
             │   Angular    │
             └──────┬───────┘
                    │
                    │ Bearer token
                    ▼
             ┌──────────────┐
             │   FastAPI    │
             └──────┬───────┘
                    │
                    ▼
          verify_firebase_token()
                    │
                    ▼
               Firebase UID
                    │
                    ▼
          get_or_create_candidate()
                    │
                    ▼
             PostgreSQL
                    │
                    ▼
              Candidate
```

---

# 10.4.21 Test It

First start PostgreSQL:

```powershell
docker compose up -d postgres
```

Then:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

You should now see:

```text
GET /health
GET /health/db
GET /health/auth
GET /api/v1/candidates/me
```

Try:

```text
GET /health/auth
```

without authentication.

Expected:

```text
401 Unauthorized
```

That's good.

Then log in through Firebase from the Angular application once we build the frontend auth flow.

---

# 10.4.22 Important Security Rule

Never do this:

```python
candidate_id = request.query_params["candidate_id"]
```

and trust it.

Instead:

```text
Verified Firebase token
        ↓
Firebase UID
        ↓
Candidate lookup
        ↓
Candidate ID
```

This gives us the ownership chain:

```text
Firebase Identity
       ↓
firebase_uid
       ↓
candidate.id
       ↓
candidate-owned resources
```

Later this will protect:

```text
/resumes
/role-profiles
/applications
/outreach
/preferences
/projects
/experiences
```

---

# 10.4.23 One More Important Design Decision

We should **not** make Firebase UID our primary database ID.

We have:

```text
Candidate.id
```

as our internal UUID.

And:

```text
Candidate.firebase_uid
```

as the external identity reference.

Why?

Because later we may support:

* another authentication provider
* enterprise SSO
* account migration
* multiple identity providers

Our domain model should not become permanently dependent on Firebase.

So:

```text
Firebase
    ↓
Identity

PostgreSQL
    ↓
Application identity
```

---

# 10.4.24 What You Should Understand for Interviews

### Authentication flow

Be able to explain:

> The frontend authenticates the user through Firebase and receives an ID token. The token is sent to FastAPI as a Bearer token. FastAPI verifies the token using Firebase Admin SDK, obtains the trusted Firebase UID, and uses that UID to identify the corresponding candidate.

### Why Admin SDK?

Because token verification must happen on the trusted backend, not in the browser.

### Why not trust the frontend UID?

Because client-side values are untrusted.

### What is a Bearer token?

A token presented by the client to prove authorization to access a protected resource.

### What is `Depends()`?

FastAPI's dependency injection mechanism. We use it to provide reusable dependencies such as database sessions and authenticated users.

---

# 10.4.25 Definition of Done

Before moving forward:

* [ ] Firebase Authentication enabled
* [ ] Firebase Admin SDK installed
* [ ] Firebase credentials secured
* [ ] Firebase initialized in backend
* [ ] Bearer token dependency created
* [ ] `/health/auth` protected
* [ ] unauthenticated request returns `401`
* [ ] Candidate linked through Firebase UID
* [ ] `/api/v1/candidates/me` created
* [ ] candidate repository works
* [ ] candidate service works
* [ ] candidate record can be created from authenticated identity
* [ ] Firebase credentials are not committed
* [ ] frontend never receives Admin SDK credentials

---

## Next — Phase 10.5: Candidate Onboarding

Now we can finally build the **first real product flow**:

```text
Login
  ↓
Candidate created
  ↓
Onboarding
  ↓
Name
Location
Experience
Education
Preferred roles
Preferred locations
Work mode
Skills
Salary expectations
Job preferences
  ↓
Candidate Profile
```

This is where our original product idea starts becoming usable: the system will begin building the **source-of-truth candidate profile** that later powers matching, resume selection, tailoring, and job discovery.
