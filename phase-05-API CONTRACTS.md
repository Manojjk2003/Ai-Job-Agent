1. Purpose of Phase 5

In Phase 4 we designed:

Angular
   ↓
FastAPI Router
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL

Now we define exactly what Angular can ask FastAPI to do.

For example:

GET /api/v1/jobs

is not enough.

We need to define:

GET /api/v1/jobs?page=1&page_size=20&location_id=...

Response:
{
    "items": [...],
    "page": 1,
    "page_size": 20,
    "total": 143,
    "has_next": true
}

This is an API contract.

2. Why API Contracts Are Important

Without contracts, frontend and backend development becomes:

Frontend developer:
"What response should I expect?"

Backend developer:
"I'll send whatever the database returns."

Frontend:
"Why is this field called company_name?"

Backend:
"I changed it to companyName."

Frontend:
"Now everything broke."

With a contract:

Frontend ─────── API Contract ─────── Backend
                    │
                    ├── Request
                    ├── Response
                    ├── Errors
                    ├── Authentication
                    └── Validation

Both sides agree before implementation.

3. API Design Principles

Our API should follow these principles:

3.1 REST-oriented

Use resources rather than action-heavy URLs.

Good:

GET /jobs
GET /jobs/{job_id}
POST /applications
GET /applications

Avoid:

POST /getAllJobs
POST /createNewApplication
POST /fetchJobDetails
3.2 Versioned APIs

All MVP APIs:

/api/v1/...

Example:

/api/v1/jobs

Later:

/api/v2/jobs

This lets us evolve the API without immediately breaking older clients.

4. Authentication Contract

The frontend uses Firebase Authentication.

Flow:

User
 │
 │ Login
 ▼
Firebase Authentication
 │
 │ Firebase ID Token
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
 │ uid
 ▼
Candidate

Every protected request uses:

Authorization: Bearer <firebase_id_token>

Example:

GET /api/v1/profile
Authorization: Bearer eyJhbGciOi...

The frontend should never send candidate_id as the authority for ownership.

The backend gets the authenticated Firebase UID and determines the candidate.

5. API Response Standards

We should keep responses consistent.

Successful single resource

Example:

{
  "id": "candidate_123",
  "full_name": "Manoj K",
  "email": "example@email.com"
}
Successful collection

Use:

{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 0,
  "has_next": false
}
6. Pagination Contract

For list APIs:

?page=1&page_size=20

Default:

page = 1
page_size = 20

Maximum:

page_size = 100

Example:

GET /api/v1/jobs?page=2&page_size=20

Response:

{
  "items": [],
  "page": 2,
  "page_size": 20,
  "total": 137,
  "has_next": true
}
7. Standard Error Contract

All errors should follow one structure:

{
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "The requested job was not found.",
    "request_id": "req_abc123"
  }
}

Possible error codes:

VALIDATION_ERROR
AUTHENTICATION_REQUIRED
INVALID_TOKEN
FORBIDDEN
NOT_FOUND
CONFLICT
JOB_NOT_FOUND
COMPANY_NOT_FOUND
PROFILE_NOT_FOUND
RESUME_NOT_FOUND
APPLICATION_NOT_FOUND
PROVIDER_ERROR
DATABASE_ERROR
RATE_LIMITED
INTERNAL_ERROR
8. Health APIs
GET /api/v1/health

Purpose:

Check whether backend is running.

Response:

{
  "status": "ok"
}
GET /api/v1/health/dependencies

Purpose:

Check important dependencies.

Example response:

{
  "status": "ok",
  "dependencies": {
    "postgresql": "ok",
    "firebase": "ok",
    "qdrant": "ok"
  }
}

This should eventually be restricted from public access if it exposes sensitive infrastructure information.

9. Candidate APIs

The candidate is the main user entity.

GET /api/v1/candidate

Get the currently authenticated candidate.

Response:

{
  "id": "candidate_123",
  "firebase_uid": "firebase_uid_123",
  "email": "user@example.com",
  "full_name": "Manoj K",
  "created_at": "2026-10-04T10:00:00Z"
}

The backend identifies the candidate using the Firebase token.

PATCH /api/v1/candidate

Update basic candidate information.

Request:

{
  "full_name": "Manoj K",
  "phone": "+91XXXXXXXXXX"
}

Response:

{
  "id": "candidate_123",
  "full_name": "Manoj K",
  "phone": "+91XXXXXXXXXX"
}
10. Candidate Profile APIs

Candidate profile contains professional information.

GET /api/v1/profile

Response:

{
  "candidate_id": "candidate_123",
  "headline": "Junior Software Engineer",
  "summary": "...",
  "years_of_experience": 1.5,
  "current_location": {
    "city": "Bengaluru",
    "state": "Karnataka",
    "country": "India"
  }
}
PUT /api/v1/profile

Create/update candidate profile.

Request:

{
  "headline": "Junior Software Engineer",
  "summary": "Software developer experienced in Angular, FastAPI and REST APIs.",
  "years_of_experience": 1.5
}
11. Experience APIs
GET /api/v1/experiences

Returns candidate's experiences.

GET /api/v1/experiences

Response:

{
  "items": [
    {
      "id": "exp_123",
      "company_name": "Example Company",
      "title": "Software Engineer",
      "employment_type": "full_time",
      "start_date": "2025-04-01",
      "end_date": null,
      "description": "..."
    }
  ]
}
POST /api/v1/experiences

Request:

{
  "company_name": "Example Company",
  "title": "Software Engineer",
  "employment_type": "full_time",
  "start_date": "2025-04-01",
  "end_date": null,
  "description": "..."
}
PATCH /api/v1/experiences/{experience_id}

Update experience.

DELETE /api/v1/experiences/{experience_id}

Delete experience.

The backend must verify that the experience belongs to the authenticated candidate.

12. Education APIs
GET    /api/v1/education
POST   /api/v1/education
PATCH  /api/v1/education/{education_id}
DELETE /api/v1/education/{education_id}

Example:

{
  "institution": "Oxford College",
  "degree": "BCA",
  "field_of_study": "Computer Applications",
  "cgpa": 7.93,
  "start_date": "2021-01-01",
  "end_date": "2024-01-01"
}
13. Project APIs
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/projects/{project_id}
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}

Example:

{
  "name": "Teacher Progress Tracking",
  "description": "...",
  "role": "Full Stack Developer",
  "technologies": [
    "Angular",
    "FastAPI",
    "MySQL",
    "AWS",
    "Docker"
  ]
}

The actual technology/skill relationships should ultimately use the normalized skill entities rather than relying only on free-text arrays.

14. Skill APIs

Skills are first-class entities.

GET /api/v1/skills

Search available normalized skills.

GET /api/v1/skills?query=angular

Response:

{
  "items": [
    {
      "id": "skill_123",
      "name": "Angular",
      "category": "frontend"
    }
  ]
}
15. Candidate Skill APIs
GET /api/v1/candidate/skills

Returns the candidate's skills.

{
  "items": [
    {
      "skill_id": "skill_123",
      "skill_name": "Angular",
      "proficiency": "intermediate",
      "years_used": 1.5
    }
  ]
}
POST /api/v1/candidate/skills

Request:

{
  "skill_id": "skill_123",
  "proficiency": "intermediate",
  "years_used": 1.5
}
16. Role Profile APIs

This is extremely important for our product.

A candidate should not have only one generic professional identity.

Example:

Candidate
 │
 ├── Frontend Developer Profile
 ├── Full Stack Developer Profile
 └── FDE Profile
GET /api/v1/role-profiles

Response:

{
  "items": [
    {
      "id": "role_123",
      "name": "Frontend Developer",
      "target_titles": [
        "Frontend Developer",
        "Angular Developer",
        "UI Developer"
      ],
      "active": true
    }
  ]
}
POST /api/v1/role-profiles

Request:

{
  "name": "Full Stack Developer",
  "target_titles": [
    "Full Stack Developer",
    "Software Engineer",
    "Backend Developer"
  ],
  "target_seniority": "junior"
}
GET /api/v1/role-profiles/{role_profile_id}

Returns complete role profile.

PATCH /api/v1/role-profiles/{role_profile_id}

Updates role profile.

DELETE /api/v1/role-profiles/{role_profile_id}

Deletes/deactivates role profile.

17. Candidate Preferences APIs

Preferences control job discovery.

Example:

{
  "preferred_locations": [
    "HSR Layout",
    "Koramangala",
    "Bengaluru"
  ],
  "remote_preference": "hybrid",
  "employment_types": [
    "full_time"
  ],
  "minimum_experience": 0,
  "maximum_experience": 3
}

API:

GET /api/v1/preferences
PUT /api/v1/preferences
18. Location APIs

Location is a major part of our product.

GET /api/v1/locations/search

Example:

GET /api/v1/locations/search?query=HSR

Response:

{
  "items": [
    {
      "id": "loc_123",
      "name": "HSR Layout",
      "city": "Bengaluru",
      "state": "Karnataka",
      "country": "India"
    }
  ]
}
19. Company APIs
GET /api/v1/companies

Supports filtering:

location
industry
company_size
search

Example:

GET /api/v1/companies?location_id=loc_123&page=1&page_size=20
GET /api/v1/companies/{company_id}

Returns company information.

Example:

{
  "id": "company_123",
  "name": "Example Technologies",
  "website": "https://example.com",
  "industry": "Software",
  "locations": [],
  "hiring_sources": []
}
20. Company Discovery API

This is one of the most important product-specific APIs.

POST /api/v1/companies/discover

Request:

{
  "location_id": "loc_123",
  "industry": "software",
  "limit": 50
}

Response:

{
  "run_id": "search_run_123",
  "status": "started"
}

Why asynchronous?

Company discovery may require:

Location
 ↓
Company discovery
 ↓
Company normalization
 ↓
Website research
 ↓
Career page detection
 ↓
Hiring source detection

This could take time.

So we should not make the browser wait for everything.

21. Hiring Source APIs
GET /api/v1/companies/{company_id}/hiring-sources

Example:

{
  "items": [
    {
      "source": "company_careers",
      "url": "https://example.com/careers",
      "status": "active",
      "confidence": 0.95,
      "last_verified_at": "2026-10-04T08:00:00Z"
    },
    {
      "source": "linkedin",
      "status": "observed",
      "confidence": 0.82
    }
  ]
}

This allows the system to learn:

Where does this company actually hire?

That is a core differentiator.

22. Job APIs
GET /api/v1/jobs

Supports:

search
location
company
role
experience
employment_type
remote
source
page
page_size

Example:

GET /api/v1/jobs?location_id=loc_123&role=frontend&page=1&page_size=20
23. Get Job
GET /api/v1/jobs/{job_id}

Response:

{
  "id": "job_123",
  "title": "Frontend Developer",
  "company": {
    "id": "company_123",
    "name": "Example Technologies"
  },
  "locations": [],
  "description": "...",
  "employment_type": "full_time",
  "experience_min": 0,
  "experience_max": 2,
  "application_url": "...",
  "sources": []
}
24. Job Sources
GET /api/v1/jobs/{job_id}/sources

Response:

{
  "items": [
    {
      "source": "company_careers",
      "external_id": "career_123",
      "url": "..."
    },
    {
      "source": "linkedin",
      "external_id": "linkedin_456",
      "url": "..."
    }
  ]
}

This preserves the fact that one canonical job may appear in multiple places.

25. Job Discovery API
POST /api/v1/jobs/discover

Request:

{
  "location_id": "loc_123",
  "role_profile_id": "role_123",
  "company_ids": [
    "company_123",
    "company_456"
  ],
  "sources": [
    "company_careers",
    "linkedin"
  ]
}

Response:

{
  "run_id": "search_run_456",
  "status": "started"
}
26. Search Run API

Long-running discovery processes need status tracking.

GET /api/v1/search-runs/{run_id}

Response:

{
  "id": "search_run_456",
  "type": "job_discovery",
  "status": "completed",
  "started_at": "2026-10-04T08:00:00Z",
  "completed_at": "2026-10-04T08:02:31Z",
  "results_count": 73
}

Possible statuses:

pending
running
completed
failed
cancelled
27. Job Analysis API

A job description can be analyzed separately.

POST /api/v1/jobs/{job_id}/analyze

Response:

{
  "job_id": "job_123",
  "analysis": {
    "role": "Frontend Developer",
    "seniority": "junior",
    "required_skills": [],
    "preferred_skills": [],
    "experience_requirements": [],
    "location_requirements": [],
    "employment_type": "full_time"
  }
}

The analysis may use Gemini, but the resulting structured data should be validated before storing.

28. Matching APIs

This is the heart of candidate-to-job evaluation.

POST /api/v1/jobs/{job_id}/match

Request:

{
  "role_profile_id": "role_123"
}

Response:

{
  "job_id": "job_123",
  "candidate_id": "candidate_123",
  "match": {
    "overall": "strong",
    "score": 82,
    "required_skills_match": 0.9,
    "experience_match": 0.8,
    "location_match": 1.0,
    "eligibility_match": 1.0
  },
  "evidence": []
}

Important:

The score is our application's analytical score, not a claim that it is the actual ATS score used by the employer.

29. Match Evidence API
GET /api/v1/jobs/{job_id}/match

Example:

{
  "strong_matches": [
    {
      "requirement": "Angular",
      "candidate_evidence": "Teacher Progress Tracking project",
      "confidence": 0.95
    }
  ],
  "partial_matches": [],
  "missing_requirements": [
    {
      "requirement": "Next.js",
      "reason": "No verified experience found."
    }
  ]
}

This makes the system explainable.

Instead of:

"You are 82% compatible."

the system can say:

"You match Angular, TypeScript, REST APIs and AWS. Next.js is missing from your verified experience."

That is much more useful.

30. Resume APIs
GET /api/v1/resumes

Returns candidate's source resumes.

POST /api/v1/resumes

Upload a resume.

The backend should:

Upload
 ↓
Validate file
 ↓
Store file
 ↓
Parse PDF/DOCX
 ↓
Extract candidate information
 ↓
Show extracted information
 ↓
User confirms/corrects
 ↓
Store verified data

We should not automatically treat extracted resume information as truth without validation.

31. Resume Selection API
POST /api/v1/jobs/{job_id}/resume-selection

Request:

{
  "role_profile_id": "role_123"
}

Response:

{
  "recommended_resume_id": "resume_123",
  "reason": "Full Stack Developer profile aligns best with this job."
}
32. Tailored Resume API
POST /api/v1/jobs/{job_id}/tailored-resume

Request:

{
  "role_profile_id": "role_123",
  "base_resume_id": "resume_123"
}

Response:

{
  "tailored_resume_id": "tailored_123",
  "status": "generated"
}

For longer generation:

{
  "run_id": "agent_run_123",
  "status": "started"
}
33. Resume Claim Validation

Before allowing a tailored resume to be finalized:

Candidate Truth
      ↓
Resume Claims
      ↓
Claim Validator
      ↓
Verified
 /       \
YES       NO
 |         |
Allow    Flag/Reject

API:

GET /api/v1/tailored-resumes/{id}/claims

Example:

{
  "items": [
    {
      "claim": "Built FastAPI backend",
      "status": "verified",
      "evidence_id": "exp_123"
    },
    {
      "claim": "Expert in Kubernetes",
      "status": "unsupported",
      "reason": "No candidate evidence found."
    }
  ]
}

This is a critical anti-fabrication mechanism.

34. Application APIs
POST /api/v1/applications

Request:

{
  "job_id": "job_123",
  "resume_id": "tailored_123"
}

Response:

{
  "id": "application_123",
  "job_id": "job_123",
  "status": "planned",
  "created_at": "2026-10-04T09:00:00Z"
}
35. Application Status

Possible statuses:

planned
applied
assessment
interview
rejected
offer
withdrawn
closed
PATCH /api/v1/applications/{application_id}

Example:

{
  "status": "applied"
}
36. Application Events

Every important application state change should create an event.

GET /api/v1/applications/{application_id}/events

Example:

{
  "items": [
    {
      "type": "created",
      "timestamp": "...",
      "metadata": {}
    },
    {
      "type": "resume_selected",
      "timestamp": "...",
      "metadata": {}
    },
    {
      "type": "applied",
      "timestamp": "...",
      "metadata": {}
    }
  ]
}

This gives us an audit trail.

37. Outreach APIs
POST /api/v1/jobs/{job_id}/outreach

Request:

{
  "contact_id": "contact_123",
  "channel": "email",
  "tone": "professional"
}

Response:

{
  "id": "outreach_123",
  "status": "draft"
}

Important:

Generation and sending are separate.

Generate
   ↓
Draft
   ↓
User Approval
   ↓
Send
38. Contacts APIs
GET  /api/v1/companies/{company_id}/contacts
POST /api/v1/companies/{company_id}/contacts

Only public/permitted contact information should be stored.

The product should not encourage harvesting private personal information.

39. Agent Run APIs

Agents may perform longer operations.

GET /api/v1/agent-runs/{run_id}

Response:

{
  "id": "agent_run_123",
  "agent_type": "job_discovery",
  "status": "running",
  "started_at": "...",
  "completed_at": null
}
40. Notifications
GET  /api/v1/notifications
PATCH /api/v1/notifications/{notification_id}

Example:

{
  "id": "notification_123",
  "type": "job_match",
  "title": "New strong job match",
  "message": "Frontend Developer at Example Technologies",
  "read": false
}
41. MVP API List

We should not implement every API immediately.

MVP priority:

Authentication
GET /api/v1/candidate
Candidate
GET /api/v1/profile
PUT /api/v1/profile

GET /api/v1/experiences
POST /api/v1/experiences
PATCH /api/v1/experiences/{id}
DELETE /api/v1/experiences/{id}

GET /api/v1/projects
POST /api/v1/projects

GET /api/v1/candidate/skills
POST /api/v1/candidate/skills
Role
GET /api/v1/role-profiles
POST /api/v1/role-profiles
GET /api/v1/role-profiles/{id}
PATCH /api/v1/role-profiles/{id}
Preferences
GET /api/v1/preferences
PUT /api/v1/preferences
Companies
GET /api/v1/companies
GET /api/v1/companies/{id}
POST /api/v1/companies/discover
Jobs
GET /api/v1/jobs
GET /api/v1/jobs/{id}
POST /api/v1/jobs/discover
GET /api/v1/search-runs/{id}
Matching
POST /api/v1/jobs/{id}/match
GET /api/v1/jobs/{id}/match
Resumes
GET /api/v1/resumes
POST /api/v1/resumes
POST /api/v1/jobs/{id}/resume-selection
POST /api/v1/jobs/{id}/tailored-resume
Applications
GET /api/v1/applications
POST /api/v1/applications
GET /api/v1/applications/{id}
PATCH /api/v1/applications/{id}
GET /api/v1/applications/{id}/events
42. Complete API Map

Our architecture now looks like:

/api/v1
│
├── /health
│
├── /candidate
├── /profile
├── /experiences
├── /education
├── /projects
├── /skills
├── /candidate/skills
│
├── /role-profiles
├── /preferences
│
├── /locations
│
├── /companies
│   ├── /discover
│   └── /{company_id}
│       ├── /hiring-sources
│       └── /contacts
│
├── /jobs
│   ├── /discover
│   └── /{job_id}
│       ├── /sources
│       ├── /analyze
│       ├── /match
│       ├── /resume-selection
│       └── /tailored-resume
│
├── /resumes
│
├── /applications
│   └── /{application_id}
│       └── /events
│
├── /outreach
│
├── /search-runs
├── /agent-runs
└── /notifications
43. Frontend ↔ Backend Contract

Angular should never directly access PostgreSQL.

Correct:

Angular
   ↓ HTTP
FastAPI
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL

Incorrect:

Angular
   ↓
PostgreSQL

Similarly, Angular should not directly call Gemini for core product operations.

Correct:

Angular
   ↓
FastAPI
   ↓
Agent/AI Service
   ↓
Gemini

This gives us security, validation, auditing and centralized business rules.

44. API → Service Mapping

Example:

POST /jobs/{id}/match
        ↓
matching.py router
        ↓
MatchingService
        ↓
MatchingRepository
        ↓
JobRepository
CandidateRepository
        ↓
Deterministic matching
        ↓
AI/semantic analysis if required
        ↓
JobMatch
        ↓
Response
45. Agent APIs Are Not the Same as Normal APIs

This distinction is important.

Normal operation:

GET job
      ↓
JobService
      ↓
Database

Agent operation:

User:
"Find frontend jobs near HSR."

        ↓

Career Orchestrator
        ↓
Company Discovery Tool
        ↓
Job Discovery Tool
        ↓
Matching Tool
        ↓
Results

The agent should use existing application capabilities.

It should not bypass the backend architecture.

46. API Security Rules

Every protected endpoint must answer:

Who is calling?

Firebase token.

What candidate do they belong to?

Firebase UID → Candidate.

Are they allowed to access this resource?

Ownership/authorization check.

Is the input valid?

Pydantic validation.

Is the operation dangerous?

Require approval.

Examples:

Read jobs             → normal
Run matching          → normal
Generate resume       → normal
Finalize resume       → approval
Send email            → approval
Submit application    → approval
Enable auto-apply     → explicit approval
47. Idempotency

Some operations may be retried.

Example:

POST /applications

The network fails.

Frontend retries.

Without protection:

Application #1
Application #2

Same job.

Bad.

We should eventually support idempotency keys for important mutation operations.

Example:

Idempotency-Key: 7c9e...

The backend can safely return the existing result instead of creating a duplicate.

48. API Documentation

FastAPI automatically provides OpenAPI documentation.

Development:

/docs

and:

/redoc

Example:

http://localhost:8000/docs

This becomes extremely useful while learning because you can inspect:

Endpoint
 ↓
Request schema
 ↓
Response schema
 ↓
Status codes
 ↓
Try API
49. Example End-to-End Flow

Suppose the user says:

"Find frontend jobs around HSR Layout."

The frontend might execute:

1. GET /locations/search?query=HSR

2. POST /companies/discover

3. GET /search-runs/{id}

4. POST /jobs/discover

5. GET /search-runs/{id}

6. GET /jobs?location_id=...

7. POST /jobs/{job_id}/match

Then UI shows:

Frontend Developer
Example Company
HSR Layout

Match: Strong

✓ Angular
✓ TypeScript
✓ REST API
✓ 1–2 years experience

△ React
△ AWS

Missing:
✗ Next.js

Then:

Create tailored resume
        ↓
POST /jobs/{id}/tailored-resume
        ↓
Claim validation
        ↓
User approval
        ↓
Application

This is the actual product flow we are designing toward.

50. API Contract Rules We Will Freeze

Before implementation:

/api/v1 versioning
Firebase Bearer authentication
consistent error structure
pagination standard
Pydantic request/response schemas
ownership checks
idempotency for sensitive mutations
async handling for long-running operations
no database access from Angular
no direct external provider calls from Angular
agents use backend tools/services
AI does not bypass validation
user approval for sensitive actions
51. What Phase 5 Gives Us

We now have the bridge:

PHASE 3
Database
   ↓
PHASE 4
Backend Architecture
   ↓
PHASE 5
API Contracts
   ↓
PHASE 6
Agent + Tool + MCP Architecture
   ↓
PHASE 7
RAG / Vector Architecture
   ↓
PHASE 8
Security
   ↓
PHASE 9
Project Setup
   ↓
PHASE 10
Implementation

The next phase is especially important because this is where we decide exactly how Google ADK agents, tools, providers and MCP fit into the system without turning the entire application into an uncontrolled AI agent.

PHASE 5 CHECKLIST

Before moving forward, Phase 5 should be considered complete when we have:

 API versioning
 Authentication contract
 Authorization model
 Standard response format
 Standard error format
 Pagination
 Candidate APIs
 Profile APIs
 Experience/Education/Project APIs
 Skill APIs
 Role Profile APIs
 Preference APIs
 Location APIs
 Company APIs
 Hiring-source APIs
 Job APIs
 Discovery APIs
 Matching APIs
 Resume APIs
 Tailored-resume APIs
 Application APIs
 Outreach APIs
 Agent-run APIs
 Notification APIs
 Human-approval boundaries
 Idempotency strategy
 MVP endpoint list
 End-to-end API flow