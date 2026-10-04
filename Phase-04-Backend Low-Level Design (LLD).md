1. Purpose

Phase 4 defines exactly how the backend will be structured internally.

We will decide:

FastAPI project structure
Routers
Services
Repositories
Database models
Pydantic schemas
Dependencies
Authentication
Authorization
Error handling
Configuration
Logging
Background processing
Provider interfaces
Agent boundaries
Transaction handling
Validation
File handling
Testing boundaries

The objective is to reach a point where Phase 9 project setup can create the actual project structure without architectural ambiguity.

2. Backend Technology

Initial backend stack:

Python
FastAPI
SQLAlchemy 2.x
PostgreSQL
Alembic
Pydantic / Pydantic Settings
httpx
Firebase Admin SDK
pytest

Later integrations:

Google ADK
Qdrant
Hugging Face embeddings
Object Storage
External Job Providers
Email Provider
3. Backend Architecture

The backend follows a modular layered architecture.

                    Client
                      │
                      ▼
                 FastAPI API
                      │
                 ┌────┴────┐
                 │ Routers │
                 └────┬────┘
                      │
                      ▼
                Dependencies
                      │
                      ▼
                 Services
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    Repositories   Providers   Agent Tools
          │           │           │
          ▼           ▼           ▼
     PostgreSQL   External APIs  ADK

The important rule is:

Routers handle HTTP concerns. Services handle business logic. Repositories handle database access.

4. Why Layered Architecture?

Without separation, a route can become:

@app.post("/jobs")
def create_job():
    validate()
    call_provider()
    calculate_match()
    insert_company()
    insert_job()
    send_email()

This becomes difficult to test and maintain.

Instead:

Router
   ↓
Service
   ↓
Repository
   ↓
Database

Each layer has a clear responsibility.

5. Recommended Backend Structure

Initial structure:

backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── router.py
│   │   │
│   │   ├── v1/
│   │   │   ├── router.py
│   │   │   │
│   │   │   ├── candidates.py
│   │   │   ├── profiles.py
│   │   │   ├── role_profiles.py
│   │   │   ├── preferences.py
│   │   │   ├── companies.py
│   │   │   ├── jobs.py
│   │   │   ├── matching.py
│   │   │   ├── resumes.py
│   │   │   ├── applications.py
│   │   │   ├── outreach.py
│   │   │   └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   └── constants.py
│   │
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   ├── models/
│   │   └── migrations/
│   │
│   ├── schemas/
│   │   ├── candidate.py
│   │   ├── profile.py
│   │   ├── role_profile.py
│   │   ├── preference.py
│   │   ├── company.py
│   │   ├── job.py
│   │   ├── matching.py
│   │   ├── resume.py
│   │   ├── application.py
│   │   └── common.py
│   │
│   ├── repositories/
│   │   ├── candidate_repository.py
│   │   ├── company_repository.py
│   │   ├── job_repository.py
│   │   ├── matching_repository.py
│   │   ├── resume_repository.py
│   │   └── application_repository.py
│   │
│   ├── services/
│   │   ├── candidate_service.py
│   │   ├── profile_service.py
│   │   ├── company_service.py
│   │   ├── job_service.py
│   │   ├── discovery_service.py
│   │   ├── matching_service.py
│   │   ├── resume_service.py
│   │   ├── application_service.py
│   │   └── outreach_service.py
│   │
│   ├── providers/
│   │   ├── base.py
│   │   ├── jobs/
│   │   ├── companies/
│   │   └── contacts/
│   │
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── candidate_agent.py
│   │   ├── company_agent.py
│   │   ├── job_agent.py
│   │   ├── matching_agent.py
│   │   └── resume_agent.py
│   │
│   ├── background/
│   │   ├── jobs.py
│   │   └── scheduler.py
│   │
│   └── utils/
│       ├── normalization.py
│       ├── pagination.py
│       └── dates.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── api/
│
├── alembic.ini
├── pyproject.toml
├── .env.example
└── README.md

This is a starting structure, not permission to create every file immediately.

6. main.py

main.py is responsible for assembling the FastAPI application.

Conceptually:

main.py
   │
   ├── create FastAPI app
   ├── configure logging
   ├── configure middleware
   ├── register exception handlers
   ├── register API router
   └── configure lifecycle

It should not contain business logic.

7. API Router Layer

The router is the HTTP boundary.

Example:

POST /api/v1/jobs/search

The router should:

Receive HTTP request.
Validate request schema.
Get authenticated candidate.
Call appropriate service.
Return response schema.

Conceptually:

HTTP Request
     ↓
Router
     ↓
Auth Dependency
     ↓
Service
     ↓
Response Schema
     ↓
HTTP Response
8. Router Responsibility

Router should handle:

HTTP methods
paths
request/response schemas
authentication dependency
query/path parameters
HTTP status codes

Router should NOT handle:

SQL queries
complex matching logic
provider-specific implementation
resume generation logic
agent reasoning
9. Service Layer

Services contain application/business logic.

Example:

JobService

may coordinate:

JobRepository
CompanyRepository
MatchingService
Provider

Example flow:

JobService
   │
   ├── normalize job
   ├── find company
   ├── create/update job
   ├── attach source
   └── return canonical job
10. Repository Layer

Repositories are responsible for database access.

Example:

JobRepository

may provide:

get_by_id()
get_by_source_id()
create()
update()
search()
list_for_company()

Repository code should not decide:

Should this job be recommended to the candidate?

That is business logic and belongs in the service/matching layer.

11. SQLAlchemy Models

SQLAlchemy models represent PostgreSQL tables.

Example conceptual model:

CandidateModel
CandidateProfileModel
RoleProfileModel
ExperienceModel
ProjectModel
SkillModel
CompanyModel
JobModel
JobSourceModel
JobMatchModel
ResumeModel
ApplicationModel

Models represent persistence.

They should not become huge business-logic containers.

12. Pydantic Schemas

Pydantic schemas represent API input/output.

Example:

CreateCandidateRequest
UpdateCandidateProfileRequest
CandidateResponse

CreateJobRequest
JobResponse

JobSearchRequest
JobSearchResponse

Important distinction:

SQLAlchemy Model
        ↓
Database representation

Pydantic Schema
        ↓
API representation

Do not automatically expose database models directly through APIs.

13. Dependency Injection

FastAPI dependencies should provide reusable infrastructure.

Examples:

get_db()
get_current_candidate()
get_candidate_service()
get_job_service()

Conceptually:

Request
   │
   ├── get_db()
   ├── get_current_user()
   └── get_service()
          │
          ▼
        Router
14. Database Session

Each request requiring database access should receive an appropriate SQLAlchemy session.

Conceptually:

HTTP Request
     ↓
get_db()
     ↓
Session
     ↓
Service
     ↓
Repository
     ↓
PostgreSQL

The session lifecycle must be controlled centrally.

Do not manually create random database connections inside services.

15. Transactions

Operations that change multiple related records should use transactions.

Example:

Create canonical job
    ↓
Create job source
    ↓
Create job skills
    ↓
Create job requirements

These should succeed or fail consistently.

BEGIN
   create job
   create source
   create skills
   create requirements
COMMIT

If something fails:

ROLLBACK
16. Authentication

Authentication is handled by Firebase Authentication.

Flow:

User
 │
 ▼
Firebase Login
 │
 ▼
Firebase ID Token
 │
 ▼
Frontend
 │
 ▼
Authorization: Bearer <token>
 │
 ▼
FastAPI
 │
 ▼
Firebase Admin SDK
 │
 ▼
Verified Firebase UID

The backend must verify the token.

The frontend cannot be trusted to tell the backend:

{
  "candidate_id": "some-id"
}

without server-side authorization.

17. Current Candidate Resolution

After verifying Firebase authentication:

Firebase UID
     ↓
CandidateRepository
     ↓
candidate.firebase_uid
     ↓
Candidate

The backend should work with the authenticated candidate identity.

This prevents one candidate from accessing another candidate's data.

18. Authorization

Authentication answers:

Who are you?

Authorization answers:

Are you allowed to access this resource?

Example:

GET /applications/123

The backend must verify:

application.candidate_id
        ==
current_candidate.id

before returning the application.

19. Resource Ownership

Candidate-owned resources include:

Profile
RoleProfile
Experience
Education
Projects
Preferences
Resumes
Applications
Outreach

Every access must enforce ownership.

Conceptually:

Current Candidate
       │
       ▼
Resource Query
       │
       └── WHERE candidate_id = current_candidate.id
20. Company and Job Authorization

Company and job data may be shared across candidates.

For example:

Company A
   ├── Job 1
   ├── Job 2
   └── Job 3

Candidate A and Candidate B can both view the same job.

However:

Candidate A's JobMatch

must not be visible to Candidate B.

Therefore:

Company / Job
    → shared

JobMatch / Application
    → candidate-owned
21. Error Handling

The backend should have consistent errors.

Example response:

{
  "error": {
    "code": "JOB_NOT_FOUND",
    "message": "The requested job was not found.",
    "request_id": "..."
  }
}

Avoid returning raw database exceptions to users.

22. Error Categories

Initial categories:

VALIDATION_ERROR
AUTHENTICATION_REQUIRED
FORBIDDEN
NOT_FOUND
CONFLICT
PROVIDER_ERROR
DATABASE_ERROR
INTERNAL_ERROR
RATE_LIMITED
23. HTTP Status Strategy

Typical mapping:

200 OK
201 CREATED
204 NO CONTENT

400 BAD REQUEST
401 UNAUTHORIZED
403 FORBIDDEN
404 NOT FOUND
409 CONFLICT
422 VALIDATION ERROR
429 TOO MANY REQUESTS

500 INTERNAL SERVER ERROR
502 BAD GATEWAY
503 SERVICE UNAVAILABLE

The API should use consistent semantics.

24. Configuration

Configuration should be environment-based.

Example:

DATABASE_URL
FIREBASE_PROJECT_ID
FIREBASE_CLIENT_EMAIL
FIREBASE_PRIVATE_KEY

QDRANT_URL

GEMINI_API_KEY

OBJECT_STORAGE_BUCKET

LOG_LEVEL
ENVIRONMENT

Never hard-code secrets.

25. Environment Separation

At minimum:

development
test
production

Potentially:

.env
.env.test
.env.production

Secrets should not be committed to Git.

Only .env.example should be committed.

26. Provider Architecture

External job sources must not be directly embedded inside business services.

Use interfaces.

Example:

JobSourceProvider
    │
    ├── CompanyCareerProvider
    ├── PermittedJobAPIProvider
    ├── UserProvidedJobProvider
    ├── LinkedInProvider
    ├── NaukriProvider
    ├── IndeedProvider
    └── WellfoundProvider

Actual provider availability depends on permitted APIs/integrations/access.

27. Job Provider Interface

Conceptually:

class JobSourceProvider:
    async def search_jobs(...):
        ...

    async def get_job(...):
        ...

    async def normalize_job(...):
        ...

    async def health_check(...):
        ...

The application should depend on this abstraction rather than a specific website.

28. Why Provider Abstraction Matters

Suppose a provider changes its API.

Without abstraction:

JobService
    ├── LinkedIn code
    ├── Naukri code
    ├── Indeed code
    └── company website code

Everything becomes tightly coupled.

With abstraction:

JobService
      ↓
JobSourceProvider
      ↓
Specific Provider

The provider can change without rewriting the entire application.

29. Company Discovery Service

Company discovery is different from job discovery.

Flow:

Location
    ↓
Company Discovery Service
    ↓
Companies
    ↓
Company normalization
    ↓
Company locations
    ↓
Hiring source discovery

This is one of the core product capabilities.

30. Job Discovery Service

Job discovery then operates on companies and their relevant sources.

Company
   ↓
Company Hiring Sources
   ↓
Provider
   ↓
Job Results
   ↓
Normalization
   ↓
Deduplication
   ↓
Canonical Jobs
31. Job Normalization

Different sources may return:

Software Engineer
Software Engineer I
SWE-1
Junior Software Engineer

The normalization pipeline should preserve the original title but may create normalized representations.

Never destroy the original source data.

32. Matching Service

The Matching Service is responsible for deterministic/application-level matching orchestration.

Input:

Candidate
RoleProfile
Job
JobRequirements
CandidateEvidence

Output:

JobMatch
MatchEvidence

Flow:

Candidate
     │
     ▼
Role Profile
     │
     ▼
Job Requirements
     │
     ▼
Matching Service
     │
     ├── Skill match
     ├── Experience match
     ├── Location match
     ├── Education/eligibility
     └── Role alignment
             │
             ▼
        JobMatch
             │
             ▼
        MatchEvidence
33. Deterministic vs AI Matching

Not everything should be delegated to an LLM.

Deterministic checks:

Location
Experience years
Employment type
Eligibility
Required skill existence
Salary constraints

AI/semantic analysis can help with:

Similar skill interpretation
Experience relevance
Project relevance
JD language understanding
Role similarity
Explanation generation

The backend should combine both.

34. Resume Service

ResumeService coordinates:

Candidate Profile
Role Profile
Verified Experience
Projects
Skills
Education
Job JD

and produces:

Resume selection
Tailoring request
Claim validation
Generated document
35. Resume Generation Safety

The resume generator must not invent information.

Flow:

Candidate Source Data
        ↓
Allowed Claims
        ↓
Resume Generation
        ↓
Claim Extraction
        ↓
Claim Validation
        ↓
Resume Version

If an AI generates:

"Implemented Kubernetes-based deployments"

but there is no verified source evidence, the claim must be rejected or flagged.

36. Application Service

ApplicationService handles:

Create application
Update application
Change status
Record events
Attach resume version

Example:

User clicks Apply
      ↓
ApplicationService
      ↓
Validate job
      ↓
Validate candidate
      ↓
Validate selected resume
      ↓
Create Application
      ↓
Create ApplicationEvent
37. Outreach Service

OutreachService handles message preparation.

Flow:

Job
 ↓
Company
 ↓
Contact
 ↓
Candidate Profile
 ↓
Role Profile
 ↓
Generate message
 ↓
Validate claims
 ↓
User approval
 ↓
Send

The initial version should require approval before sending.

38. Background Processing

Some operations should not block an HTTP request.

Examples:

Large job discovery
Resume generation
Embedding generation
Company enrichment
Batch matching
Scheduled scans

Initial MVP can use FastAPI background tasks for lightweight work.

For heavier workloads, introduce a proper queue later.

39. Scheduler

Scheduled discovery may eventually run:

Every morning
    ↓
Candidate preferences
    ↓
Company discovery
    ↓
Job discovery
    ↓
Matching
    ↓
Notification

APScheduler can be used during local/MVP development.

The architecture should allow migration to a production queue later.

40. Agent Boundary

Agents should not directly manipulate the database arbitrarily.

Recommended flow:

Agent
  ↓
Tool
  ↓
Service
  ↓
Repository
  ↓
Database

Not:

Agent
  ↓
Raw SQL
41. Google ADK Integration

Google ADK will orchestrate agent behavior.

Conceptually:

Career Orchestrator
        │
        ├── Candidate Agent
        ├── Company Agent
        ├── Job Discovery Agent
        ├── Matching Agent
        └── Resume Agent

Agents use application tools.

42. Tool Boundary

Example tools:

search_companies()
get_company()
discover_hiring_sources()

search_jobs()
get_job()
normalize_job()

analyze_job()
match_candidate()

get_candidate_profile()
get_role_profile()

select_resume()
generate_tailored_resume()

create_application()
generate_outreach()

Tools should enforce authorization and validation.

43. MCP Boundary

MCP is treated as an integration/tool protocol, not the entire backend architecture.

Possible MCP-connected capabilities later:

GitHub
Email
Company research
External job systems
Internal career tools

The core FastAPI application remains responsible for business state.

44. Request Flow Example — Job Search

User requests:

Find frontend jobs around HSR Layout.

Flow:

Angular
   ↓
POST /api/v1/jobs/search
   ↓
FastAPI Router
   ↓
Authentication
   ↓
JobDiscoveryService
   ↓
CandidatePreferenceRepository
   ↓
CompanyDiscoveryService
   ↓
Company Providers
   ↓
Hiring Source Discovery
   ↓
Job Providers
   ↓
Job Normalization
   ↓
Deduplication
   ↓
PostgreSQL
   ↓
MatchingService
   ↓
Response
45. Request Flow Example — Tailored Resume
User selects Job
       ↓
POST /api/v1/resumes/tailor
       ↓
Authentication
       ↓
ResumeService
       ↓
Load Candidate
       ↓
Load RoleProfile
       ↓
Load Verified Experience
       ↓
Load Job
       ↓
Generate tailored content
       ↓
Validate claims
       ↓
Create ResumeVersion
       ↓
Store document
       ↓
Return preview metadata
46. Request Flow Example — Application
User approves application
        ↓
POST /api/v1/applications
        ↓
Authentication
        ↓
ApplicationService
        ↓
Validate candidate ownership
        ↓
Validate job
        ↓
Validate resume
        ↓
Create Application
        ↓
Create ApplicationEvent
        ↓
Audit Log
        ↓
Response
47. API Versioning

Use:

/api/v1/

Example:

/api/v1/candidates/me
/api/v1/jobs
/api/v1/jobs/search
/api/v1/applications

Future breaking changes can use:

/api/v2/
48. Pagination

Large collections should not return everything.

Example:

GET /api/v1/jobs?page=1&page_size=20

Response:

{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 100
}

Later, cursor pagination can be introduced for large feeds.

49. Filtering

Job listing should support filters such as:

location
role
experience
salary
work mode
company
skills
posted date
match status

Filtering should be handled by repository/query logic, not by loading everything into Python.

50. Logging

Backend logs should provide enough information to debug requests.

Useful fields:

request_id
candidate_id
route
method
status
duration
error_code

Do not log:

passwords
tokens
private credentials
unnecessary resume content
sensitive personal information
51. Observability

Later the system should provide:

Request logs
Agent traces
Provider execution logs
Database errors
Job discovery statistics
Matching statistics
Application events

Agent runs and tool calls should connect back to a request/search run where appropriate.

52. Testing Architecture

Testing layers:

Unit Tests
    ↓
Service/Utility logic

Integration Tests
    ↓
Repository + PostgreSQL

API Tests
    ↓
FastAPI endpoints

Provider Tests
    ↓
Provider normalization

Agent Evaluation
    ↓
Agent outputs
53. Unit Test Example

Test:

Skill normalization

Input:

"Postgres"

Expected:

"postgresql"

Another:

"React.js"

Expected canonical skill:

"react"
54. Service Test Example

Given:

Candidate:
Angular
TypeScript
FastAPI

Job:
Angular
TypeScript
Kubernetes

The matching service should produce structured evidence rather than only an unexplained number.

55. Repository Test Example

Test:

get_jobs_by_company()

Verify:

correct company
correct filters
pagination
status handling
no cross-company leakage
56. API Security Test

A candidate must not access another candidate's application.

Example:

Candidate A
    ↓
GET /applications/B_APPLICATION_ID

Expected:

403 Forbidden

or an appropriate not-found behavior that does not expose resource existence.

57. Service Dependency Rule

Recommended dependency direction:

Router
  ↓
Service
  ↓
Repository
  ↓
Database

and:

Service
  ↓
Provider interface
  ↓
Provider implementation

Avoid:

Repository → Router
Database Model → Service
Provider → Router

This keeps dependencies predictable.

58. Business Logic Location

Use this rule:

Logic	Location
HTTP path	Router
Request validation	Pydantic
Authentication	Security dependency
Authorization	Dependency/service
Business rules	Service
SQL queries	Repository
DB schema	SQLAlchemy model
External API call	Provider
Agent orchestration	Agent layer
Formatting/normalization	Utility/domain logic
59. Database Model vs Domain Logic

Do not put all business logic inside SQLAlchemy models.

For example:

Bad:

job.match_candidate(candidate)

when this requires multiple services/providers/configuration.

Better:

MatchingService
    ↓
JobRepository
CandidateRepository
SkillRepository

The model represents data.

The service represents business behavior.

60. MVP Simplification

Although the architecture is designed for production growth, the MVP should remain a modular monolith.

We do NOT need:

20 microservices
Kafka
Kubernetes
Redis cluster
complex event bus
multiple databases

at the beginning.

Instead:

Angular
   ↓
FastAPI modular monolith
   ↓
PostgreSQL
   ↓
Qdrant
   ↓
Object Storage

This gives speed without architectural debt.

61. First MVP Backend Modules

Build these first:

Authentication
Candidate Profile
Role Profile
Preferences
Companies
Locations
Jobs
Matching
Resumes
Applications

Then add:

Discovery providers
Outreach
Agent orchestration
Scheduler
Notifications
62. Backend Implementation Order

When we reach implementation:

1. Project setup
2. Configuration
3. Database connection
4. Alembic
5. Base SQLAlchemy models
6. Authentication
7. Candidate/profile APIs
8. Role profiles/preferences
9. Company/location models
10. Job models
11. Job discovery provider abstraction
12. Matching
13. Resume management
14. Tailoring
15. Applications
16. Background processing
17. Agent tools
18. Google ADK orchestration
19. Qdrant integration
20. Testing

This is deliberately different from trying to build the entire agent first.

63. Important Architecture Rule

The AI layer is not the application itself.

The application is:

Frontend
    +
Backend
    +
Database
    +
Providers
    +
AI/Agents

AI should enhance the product rather than control every operation.

For example:

Create application record
→ deterministic backend operation

Check ownership
→ deterministic backend operation

Save resume
→ deterministic backend operation

Find semantically similar experience
→ AI/vector capability

Understand JD
→ AI capability

Generate tailored resume
→ AI capability
64. Human Approval Boundaries

The initial system should require user approval for sensitive actions.

Resume generated
      ↓
USER APPROVAL

Outreach generated
      ↓
USER APPROVAL

Application ready
      ↓
USER APPROVAL

Automation rule enabled
      ↓
USER APPROVAL

This prevents an agent from unexpectedly taking external actions.

65. Phase 4 Completion Checklist

Phase 4 is complete when:

 FastAPI layered architecture defined
 Router responsibilities defined
 Service responsibilities defined
 Repository responsibilities defined
 SQLAlchemy model responsibility defined
 Pydantic schema responsibility defined
 Dependency injection defined
 Database session strategy defined
 Transaction strategy defined
 Firebase authentication flow defined
 Authorization strategy defined
 Resource ownership rules defined
 Error handling defined
 Configuration strategy defined
 Provider abstraction defined
 Company discovery flow defined
 Job discovery flow defined
 Matching service defined
 Resume service defined
 Application service defined
 Background processing defined
 Agent boundary defined
 MCP boundary defined
 Logging/observability defined
 Testing architecture defined
 MVP implementation order defined
 Modular-monolith strategy confirmed