# Phase 2 — High-Level Design (HLD)
## AI Career & Job Discovery Agent

**Project:** AI Career & Job Discovery Agent  
**Phase:** 2 — High-Level Design  
**Status:** Completed  
**Next Phase:** Phase 3 — Database / ERD  
**Primary stack:** Angular + FastAPI + PostgreSQL + Qdrant + Firebase Auth + Google ADK + Gemini

---

# 1. Purpose of This Document

This document defines the **High-Level Design (HLD)** of the AI Career & Job Discovery Agent.

The HLD answers:

- What are the major parts of the system?
- What responsibility does each part have?
- How do the parts communicate?
- Where is data stored?
- Which operations are synchronous?
- Which operations should run asynchronously?
- Where does AI/agent orchestration fit?
- How are external job sources isolated from the core application?
- How does the company-first, location-first job discovery strategy work?

This document intentionally does **not** define detailed classes, individual functions, database columns, or exact API request/response schemas. Those belong to later phases.

---

# 2. Architecture Goals

The architecture should support the following goals.

## 2.1 Candidate-first design

The system should maintain a reliable representation of the candidate instead of treating a resume as the complete candidate profile.

The candidate has:

- identity
- personal/professional information
- skills
- experience
- projects
- education
- certifications
- achievements
- preferences
- locations
- role interests
- multiple role-specific profiles
- multiple resumes

The resume is a generated/presented representation of verified candidate information.

---

## 2.2 Company-first and location-first discovery

The core discovery strategy is:

```text
Candidate chooses location
        ↓
Find companies in/around that location
        ↓
Understand how each company hires
        ↓
Check permitted job sources
        ↓
Find current openings
        ↓
Normalize and deduplicate jobs
        ↓
Match jobs to candidate
```

Example:

```text
HSR Layout, Bengaluru
        ↓
Company A
Company B
Company C
Company D
        ↓
For each company:
    ├── Official careers page
    ├── LinkedIn
    ├── Naukri
    ├── Indeed
    ├── Wellfound
    └── Other permitted source
        ↓
Current relevant jobs
```

The system should not assume that every company uses the same hiring channel.

---

# 3. Architecture Principles

## 3.1 Modular monolith first

The initial product should be a **modular monolith**, not microservices.

```text
Angular
   ↓
FastAPI
   ↓
Domain modules
   ↓
PostgreSQL / Qdrant / Storage
```

Why?

- simpler local development
- easier debugging
- fewer deployment problems
- lower infrastructure cost
- easier transactions
- easier learning
- sufficient for the MVP

The modules should still have clear boundaries so that a future service split is possible.

---

## 3.2 PostgreSQL is the source of truth

PostgreSQL stores authoritative business data.

Examples:

- candidates
- profiles
- skills
- experiences
- companies
- locations
- jobs
- job sources
- resumes
- applications
- outreach
- agent runs
- preferences
- audit records

Qdrant is not the source of truth.

---

## 3.3 Vector search is a supporting capability

Qdrant is used for semantic retrieval.

Examples:

- resume ↔ job similarity
- skill semantic matching
- similar jobs
- similar candidate evidence
- semantic company/job descriptions

The system should always be able to identify the underlying PostgreSQL record.

---

## 3.4 AI is not the source of truth

AI can:

- analyze
- summarize
- classify
- generate
- compare
- recommend actions based on configured rules

AI must not silently create false candidate information.

For example:

```text
Candidate does not know React
        ↓
AI must NOT add React to the resume
```

Instead:

```text
Candidate does not know React
        ↓
Match analysis
        ↓
Missing skill: React
```

---

## 3.5 Deterministic operations should remain deterministic

Not everything should be handled by an agent.

For example:

- authentication
- authorization
- database CRUD
- file validation
- duplicate detection rules
- application status changes
- audit logging
- permission checks

should primarily use normal application code.

Agents are used where reasoning is useful.

---

# 4. System Context

At the highest level:

```text
                         ┌──────────────────────┐
                         │      Candidate       │
                         │      Web Browser     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Angular Frontend     │
                         │ UI + State + Auth    │
                         └──────────┬───────────┘
                                    │ HTTPS
                                    ▼
                         ┌──────────────────────┐
                         │ FastAPI Backend      │
                         │ Application API      │
                         └──────────┬───────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
        ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
        │ PostgreSQL  │      │   Qdrant    │      │ File/Object │
        │ Source of   │      │ Vector      │      │ Storage     │
        │ Truth       │      │ Search      │      │ Resumes     │
        └─────────────┘      └─────────────┘      └─────────────┘

                         ┌──────────────────────┐
                         │ Google ADK           │
                         │ Agent Orchestration  │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼──────────────────┐
                  │                 │                  │
                  ▼                 ▼                  ▼
          Candidate Agent   Company Agent      Job Discovery Agent
                  │                 │                  │
                  └─────────────────┼──────────────────┘
                                    ▼
                         Matching / Resume /
                         Application Agents
                                    │
                                    ▼
                         Provider / Tool Layer
                                    │
             ┌──────────────────────┼─────────────────────┐
             ▼                      ▼                     ▼
       Company Careers       Permitted Job APIs      Other Integrations
```

---

# 5. Major System Components

## 5.1 Angular Frontend

The frontend is the user's main interface.

Responsibilities:

- registration/login UI
- onboarding
- candidate profile
- resume management
- role profile management
- location preferences
- company discovery
- job discovery
- match results
- resume tailoring
- application tracking
- outreach approval
- chatbot/career assistant
- settings
- notifications

The frontend should not directly communicate with external job providers.

Instead:

```text
Angular
   ↓
FastAPI
   ↓
Provider layer
   ↓
External source
```

---

# 6. Firebase Authentication

Firebase Authentication handles identity.

Responsibilities:

- registration
- login
- session/token management
- supported authentication methods
- password/account recovery

The backend verifies the Firebase identity token.

Conceptually:

```text
Browser
   │
   │ Firebase login
   ▼
Firebase Auth
   │
   │ authenticated identity
   ▼
Angular
   │
   │ Bearer token
   ▼
FastAPI
   │
   │ verify token
   ▼
Candidate identity
```

Firebase Auth identifies the user.

PostgreSQL stores the application's candidate/business information.

---

# 7. FastAPI Backend

FastAPI is the main application/backend layer.

It is responsible for:

- API endpoints
- authentication verification
- authorization
- business logic
- database access
- file handling
- orchestration entry points
- background task initiation
- provider coordination
- validation
- audit logging

Conceptually:

```text
HTTP Request
     ↓
FastAPI Router
     ↓
Authentication
     ↓
Authorization
     ↓
Application Service
     ↓
Domain Logic
     ↓
Repository / Provider / Agent
     ↓
Response
```

---

# 8. Backend Domain Modules

The backend should be organized by business capability.

Initial logical modules:

```text
auth
candidate
profile
resume
company
location
job
matching
application
outreach
agent
integration
notification
audit
```

These are logical boundaries inside the modular monolith.

They do not need to become separate deployments.

---

# 9. Candidate/Profile Module

The Candidate module manages the source-of-truth candidate profile.

It contains concepts such as:

```text
Candidate
 ├── Personal information
 ├── Preferences
 ├── Role profiles
 ├── Experiences
 ├── Education
 ├── Projects
 ├── Skills
 ├── Certifications
 └── Achievements
```

The important design rule is:

> A resume is generated from verified candidate information; the resume itself should not become the only source of candidate truth.

---

# 10. Role Profile Architecture

A candidate may target multiple roles.

Example:

```text
Candidate
   │
   ├── Full Stack Profile
   │      ├── Angular
   │      ├── FastAPI
   │      ├── MySQL
   │      └── AWS
   │
   ├── Frontend Profile
   │      ├── Angular
   │      ├── TypeScript
   │      └── React
   │
   └── FDE Profile
          ├── Requirements
          ├── HLD / LLD
          ├── APIs
          ├── Deployment
          └── Customer/problem solving
```

This prevents the system from forcing one resume onto every job.

---

# 11. Resume Module

The Resume module manages:

- uploaded source resumes
- parsed resume information
- resume versions
- role-specific resumes
- tailored resumes
- validation
- generated documents

Flow:

```text
Master Candidate Profile
        ↓
Role Profile
        ↓
Job Description
        ↓
Resume Agent
        ↓
Tailored Resume
        ↓
Claim Validation
        ↓
Candidate Approval
        ↓
Final Resume
```

The generated resume must be based on verified information.

---

# 12. Company Module

The Company module represents companies discovered by the system.

A company can have:

- company identity
- website
- locations
- industry/domain
- company size information where available
- hiring sources
- jobs
- public contacts
- discovery metadata

Example:

```text
Company
  ├── Website
  ├── Locations
  ├── Hiring Sources
  ├── Jobs
  └── Public Contacts
```

---

# 13. Location Module

Location is a first-class concept.

The system should support:

```text
Country
  ↓
State
  ↓
City
  ↓
Area / locality
  ↓
Radius / nearby area
```

Example:

```text
India
 └── Karnataka
      └── Bengaluru
           └── HSR Layout
```

Future geographic expansion may use PostGIS if advanced radius/geospatial queries become necessary.

For MVP, normal PostgreSQL location data can be sufficient.

---

# 14. Hiring Source Intelligence

One important differentiator is learning how a company actually hires.

The system should represent:

```text
Company
   │
   ├── Official Careers
   ├── LinkedIn
   ├── Naukri
   ├── Indeed
   ├── Wellfound
   └── Other permitted sources
```

A company-source relationship can store information such as:

- source
- status
- last observed
- last verified
- discovery method
- confidence
- notes/metadata

This allows the system to learn that different companies use different hiring channels.

---

# 15. Job Module

The Job module manages normalized job records.

A canonical job can have multiple source records.

Example:

```text
Canonical Job
      │
      ├── Company Careers source
      ├── LinkedIn source
      └── Naukri source
```

This avoids showing the same opening three times.

Each source record should preserve:

- source
- external ID where available
- source URL
- observed timestamp
- raw/normalized metadata as appropriate

---

# 16. Provider Layer

External job platforms must not be tightly coupled to business logic.

Define a common provider interface conceptually:

```text
JobSourceProvider
    ├── search_jobs()
    ├── get_job()
    ├── normalize_job()
    └── health_check()
```

Possible implementations:

```text
CompanyCareerProvider
PermittedJobAPIProvider
UserProvidedJobProvider
LinkedInProvider
NaukriProvider
IndeedProvider
WellfoundProvider
```

The exact implementation depends on available official/permitted access.

The system must not assume unrestricted scraping access.

---

# 17. Why the Provider Layer Matters

Without provider isolation:

```text
Matching Logic
     ↓
LinkedIn scraping code
     ↓
Naukri scraping code
     ↓
Indeed scraping code
```

This creates a fragile system.

With provider isolation:

```text
Matching Logic
     ↓
Job Provider Interface
     ↓
┌───────────┬──────────┬──────────┐
│ LinkedIn  │ Naukri   │ Indeed   │
└───────────┴──────────┴──────────┘
```

If one provider changes, the core matching/application system should not need to be rewritten.

---

# 18. Job Discovery Flow

The primary company-first discovery flow is:

```text
User selects:
HSR Layout + Frontend

        ↓

Location Discovery

        ↓

Companies in/around HSR Layout

        ↓

Company Research

        ↓

Hiring Source Discovery

        ↓

Permitted Source Queries

        ↓

Raw Job Results

        ↓

Normalization

        ↓

Duplicate Detection

        ↓

Canonical Jobs

        ↓

Candidate Matching

        ↓

Relevant Jobs
```

---

# 19. Job Normalization

Different sources may represent the same job differently.

Example:

```text
LinkedIn:
"Software Engineer - Frontend"

Company:
"Frontend Software Engineer"

Naukri:
"Frontend Developer"
```

The system should normalize:

- title
- company
- location
- employment type
- description
- skills
- experience
- salary when available
- source
- application URL
- posted/observed timestamps

Then compare records to identify likely duplicates.

---

# 20. Matching Module

Matching should combine deterministic rules and semantic analysis.

Possible signals:

```text
Candidate Role Profile
        +
Required Skills
        +
Preferred Skills
        +
Experience
        +
Location
        +
Employment Type
        +
Education / Eligibility
        +
Semantic Similarity
        ↓
Match Analysis
```

Instead of presenting an unexplained universal score, the system should provide evidence.

Example:

```text
Strong match:
- Angular
- TypeScript
- REST APIs
- 1–2 years experience

Partial:
- AWS requirement partially supported

Missing:
- Kubernetes
```

The exact scoring methodology can be defined later.

---

# 21. Qdrant Vector Architecture

Qdrant is used for semantic retrieval.

Potential collections:

```text
candidate_evidence
job_descriptions
skills
companies
resume_sections
```

Example:

```text
Candidate Experience
        ↓
Embedding Model
        ↓
Vector
        ↓
Qdrant
```

Job:

```text
Job Description
        ↓
Embedding Model
        ↓
Vector
        ↓
Qdrant
```

Then:

```text
Candidate Vector
       ↕
Semantic Search
       ↕
Job Vector
```

Qdrant results should map back to PostgreSQL entities.

---

# 22. Local Embeddings

The initial design uses a local Hugging Face embedding model.

Benefits:

- low/no API cost
- privacy
- reproducibility
- local development
- provider independence

The embedding model should be abstracted so it can later be replaced.

Conceptually:

```text
EmbeddingProvider
      ├── LocalHuggingFaceEmbeddingProvider
      └── FutureCloudEmbeddingProvider
```

---

# 23. Google ADK

Google ADK is the initial agent orchestration framework.

ADK is responsible for coordinating agent workflows.

Example:

```text
Career Orchestrator
        │
        ├── Candidate Agent
        ├── Company Agent
        ├── Job Discovery Agent
        ├── Matching Agent
        ├── Resume Agent
        └── Application Agent
```

Agents should use controlled tools rather than directly accessing arbitrary external systems.

---

# 24. Agent Responsibilities

## Candidate Agent

Used for:

- understanding candidate information
- profile analysis
- role profile assistance
- skill interpretation

## Company Agent

Used for:

- company research
- hiring source analysis
- public company information summarization

## Job Discovery Agent

Used for:

- discovering jobs
- interpreting search intent
- coordinating permitted providers
- identifying relevant openings

## Matching Agent

Used for:

- JD interpretation
- candidate-job comparison
- evidence extraction
- skill gap explanation

## Resume Agent

Used for:

- selecting appropriate resume/profile
- tailoring resume content
- rewriting verified experience for relevance
- validating claims

## Application Agent

Used for:

- application preparation
- outreach drafting
- application workflow assistance
- tracking updates

---

# 25. Agent vs Normal Code

Use normal code when the task is deterministic.

```text
Login
→ Normal code

Save candidate
→ Normal code

Check authorization
→ Normal code

Store application
→ Normal code

Validate file extension
→ Normal code
```

Use an agent when reasoning is valuable.

```text
Understand candidate intent
→ Agent

Analyze job description
→ Agent

Compare nuanced experience
→ Agent

Tailor resume wording
→ Agent

Draft personalized outreach
→ Agent
```

This separation is important for reliability and cost.

---

# 26. MCP / Tool Boundary

MCP should be treated as an integration/tool boundary, not as the entire architecture.

Conceptually:

```text
Agent
  ↓
Tool
  ↓
Provider / Integration
  ↓
External System
```

Examples of future tools:

- company research tool
- job search tool
- resume parser tool
- email tool
- GitHub profile tool
- application tracking tool

MCP should be introduced where it provides meaningful interoperability or reusable tool access.

---

# 27. Application Module

The Application module tracks the candidate's interaction with jobs.

Example lifecycle:

```text
Discovered
    ↓
Reviewed
    ↓
Matched
    ↓
Resume Prepared
    ↓
Application Started
    ↓
Applied
    ↓
Interview
    ↓
Offer
```

Other outcomes:

```text
Rejected
Withdrawn
Expired
No Response
```

The exact state machine will be defined in later API/database design.

---

# 28. Outreach Module

The system may generate personalized messages for:

- recruiter
- HR
- hiring manager
- founder
- company contact

The system should first identify the appropriate contact/context.

Example:

```text
Job
 ↓
Company
 ↓
Public contact research
 ↓
Context analysis
 ↓
Draft outreach
 ↓
Candidate approval
 ↓
Send
```

Sending should require explicit approval during the initial product stages.

---

# 29. Human Approval Boundaries

High-impact actions should not happen automatically by default.

Require candidate approval for:

```text
Final resume
        ↓
Approve

Outreach message
        ↓
Approve

Application submission
        ↓
Approve

External account integration
        ↓
Approve
```

Later, users may configure controlled automation rules.

Example:

```text
Auto-apply only when:
- location matches
- role profile matches
- salary meets threshold
- no missing mandatory skill
- candidate enabled automation
```

---

# 30. Resume Tailoring Flow

```text
Job Description
      ↓
JD Analysis
      ↓
Candidate Matching
      ↓
Select Role Profile
      ↓
Select Base Resume
      ↓
Extract Relevant Verified Evidence
      ↓
Generate Tailored Resume
      ↓
Claim Validation
      ↓
Candidate Review
      ↓
Approved Resume
```

The system must prevent unsupported claims.

---

# 31. Resume Claim Validation

Before finalizing a tailored resume:

```text
Generated Claim
      ↓
Check against candidate source-of-truth
      ↓
Supported?
 ┌────┴────┐
Yes        No
 │          │
Keep       Reject / revise
```

Example:

Candidate profile:

```text
Angular
FastAPI
MySQL
Docker
AWS
```

JD:

```text
Kubernetes
```

The resume agent must not convert:

```text
"Missing Kubernetes"
```

into:

```text
"Kubernetes experience"
```

Instead it may identify Kubernetes as a gap.

---

# 32. File and Object Storage

Generated/uploaded files should not be stored directly as large database blobs unless there is a specific reason.

Use object storage for:

- uploaded resumes
- generated resumes
- generated documents
- supporting files

PostgreSQL stores metadata and references.

Conceptually:

```text
PostgreSQL
   │
   └── file metadata + storage key

Object Storage
   │
   └── actual file
```

Initial storage can be Firebase Storage or an S3-compatible option.

---

# 33. Background Processing

Some tasks should not block an HTTP request.

Examples:

- scanning many companies
- checking multiple job providers
- parsing a large resume
- generating embeddings
- scheduled job discovery
- periodic source verification

Initial architecture:

```text
FastAPI
   ↓
Background Task / Scheduler
   ↓
Long-running operation
   ↓
PostgreSQL status updates
```

APScheduler can be used for local scheduled jobs.

A queue such as Redis/Celery or another worker architecture can be introduced later if scale requires it.

---

# 34. Synchronous vs Asynchronous Operations

## Synchronous

Suitable for:

```text
Login
Get profile
Update profile
Get job details
Get application status
```

## Asynchronous

Suitable for:

```text
Discover 500 companies
Scan many job sources
Generate embeddings for many jobs
Scheduled job scans
Bulk resume processing
Large company research
```

The frontend should show job/run status for long-running operations.

Example:

```text
Search started
     ↓
Running
     ↓
Sources checked: 7/12
     ↓
Completed
```

---

# 35. Agent Run Tracking

Agent operations should be observable.

Track concepts such as:

- agent run
- agent type
- start time
- end time
- status
- tools used
- errors
- related candidate/job/company
- evaluation metadata where applicable

Example:

```text
Agent Run
  ├── Job Discovery
  ├── Candidate ID
  ├── Location
  ├── Sources checked
  ├── Results
  └── Status
```

This will be important for debugging AI behavior.

---

# 36. Observability

The system should provide visibility into:

```text
API requests
Database errors
Provider failures
Agent runs
Tool calls
Background tasks
Resume generation
Job discovery runs
```

Logging should avoid exposing secrets or sensitive credentials.

---

# 37. Error Isolation

An external provider failure should not break the entire job discovery process.

Example:

```text
Company Careers → Success
LinkedIn → Success
Naukri → Failed
Indeed → Success
```

The result should be:

```text
Discovery completed with partial provider failure
```

not:

```text
Entire discovery failed
```

Provider errors should be recorded for observability.

---

# 38. Security Architecture

High-level security boundaries:

```text
Browser
   ↓ HTTPS
Firebase Auth
   ↓ token
FastAPI
   ↓ authorization
Application Services
   ↓
Database / Providers
```

Security responsibilities include:

- Firebase token validation
- authorization
- input validation
- secure file validation
- rate limiting
- audit logging
- secret management
- provider credential isolation
- least privilege
- safe external requests
- agent tool restrictions

The LLM itself is not a security boundary.

---

# 39. Data Ownership

A useful ownership rule:

```text
Firebase Auth
→ Identity

PostgreSQL
→ Business truth

Qdrant
→ Semantic retrieval

Object Storage
→ Files

Provider Systems
→ External source truth

Agent
→ Reasoning/orchestration
```

The application should not treat generated AI output as authoritative business data without validation.

---

# 40. Main End-to-End Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                        USER / BROWSER                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    ANGULAR FRONTEND                         │
│                                                             │
│ Dashboard | Profile | Jobs | Companies | Resume | Chat     │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                        │
│                                                             │
│ Auth | Candidate | Company | Job | Match | Resume          │
│ Application | Outreach | Agent | Integration | Audit       │
└───────────────┬─────────────────┬───────────────────────────┘
                │                 │
                │                 │
                ▼                 ▼
      ┌────────────────┐   ┌─────────────────┐
      │ PostgreSQL     │   │ Object Storage  │
      │ Source of Truth│   │ Resume/Files    │
      └────────────────┘   └─────────────────┘
                │
                ▼
        ┌────────────────┐
        │ Qdrant         │
        │ Vector Search  │
        └────────────────┘

                ┌─────────────────────────────┐
                │ Google ADK                 │
                │ Agent Orchestration        │
                └──────────────┬──────────────┘
                               │
        ┌──────────────────────┼─────────────────────────┐
        ▼                      ▼                         ▼
 Candidate Agent        Company Agent           Job Discovery Agent
        │                      │                         │
        └──────────────────────┼─────────────────────────┘
                               ▼
                       Matching / Resume /
                       Application Agents
                               │
                               ▼
                     Provider / Tool Layer
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
       Company Careers   Permitted Job APIs   Integrations
```

---

# 41. Key User Scenario — Find Jobs Around a Location

Example:

> "Find frontend jobs around HSR Layout."

Flow:

```text
Angular
   ↓
POST/search request
   ↓
FastAPI
   ↓
Job Discovery service
   ↓
Location search
   ↓
Company discovery
   ↓
Company hiring-source lookup
   ↓
Provider calls
   ↓
Normalize jobs
   ↓
Deduplicate
   ↓
Candidate matching
   ↓
Persist results
   ↓
Angular displays jobs
```

AI is used where interpretation/reasoning is useful.

Normal application code handles storage, permissions, normalization, and deterministic rules.

---

# 42. Key User Scenario — Tailor Resume

```text
User selects job
      ↓
FastAPI
      ↓
Load candidate role profile
      ↓
Load verified experience/skills
      ↓
Load job description
      ↓
Matching analysis
      ↓
Resume Agent
      ↓
Generate tailored content
      ↓
Claim validation
      ↓
Save draft
      ↓
User reviews
      ↓
Final document generated
```

---

# 43. Key User Scenario — Application Tracking

```text
User applies
     ↓
Application record
     ↓
Application events
     ↓
Status updates
     ↓
Dashboard
```

Example:

```text
Application #1024

Job: Frontend Developer
Company: Example Company

Status:
Applied

Timeline:
10 Oct → Discovered
10 Oct → Resume tailored
11 Oct → Applied
```

---

# 44. Key User Scenario — Career Chatbot

The chatbot is a career-system interface.

Example:

> "Why is this job only a partial match?"

Flow:

```text
Chat UI
   ↓
FastAPI
   ↓
Career Agent
   ↓
Retrieve job + candidate evidence
   ↓
Matching tools
   ↓
Reasoning
   ↓
Evidence-based response
```

It should answer using the user's actual application data rather than behaving like a generic chatbot.

---

# 45. External Integration Strategy

External systems should be connected through adapters/providers.

```text
Core Application
       ↓
Integration Interface
       ↓
Provider
       ↓
External System
```

This protects the core architecture from provider-specific changes.

Potential integrations:

- job sources
- email
- GitHub
- company research
- calendar
- notification systems

Only integrations that are useful and permitted should be enabled.

---

# 46. MVP Deployment Topology

For the initial local/free build:

```text
Local Machine
│
├── Angular dev server
├── FastAPI
├── PostgreSQL
├── Qdrant Docker container
├── Local embedding model
└── APScheduler
```

External services:

```text
Firebase Auth
Gemini
Firebase Storage / S3-compatible storage
Permitted external job sources
```

Docker can later package the application components.

---

# 47. Future Production Topology

A future deployment may look like:

```text
Internet
   ↓
Frontend Hosting
   ↓
API Gateway / HTTPS
   ↓
FastAPI Application
   ├── PostgreSQL
   ├── Qdrant
   ├── Object Storage
   ├── Worker / Queue
   ├── Scheduler
   └── Agent Runtime
             ↓
       External Providers
```

The exact cloud provider is intentionally not locked at HLD stage.

---

# 48. Scalability Strategy

The first version should optimize for simplicity.

Scaling path:

```text
Modular Monolith
       ↓
Background Workers
       ↓
Queue
       ↓
Provider-specific workers
       ↓
Read replicas / caching
       ↓
Service extraction only where justified
```

Do not create microservices before there is a real operational reason.

---

# 49. Reliability Strategy

Important reliability mechanisms:

- provider timeouts
- retries where safe
- idempotency
- duplicate detection
- partial-failure handling
- job run status
- agent run tracking
- database transactions
- audit logs
- validation before persistence
- human approval for high-impact actions

---

# 50. Architecture Decisions

## Decision 1 — PostgreSQL

Chosen because the domain contains many related entities and transactional workflows.

## Decision 2 — Qdrant

Chosen for semantic/vector retrieval without making vectors the business source of truth.

## Decision 3 — Modular monolith

Chosen to reduce complexity during MVP development.

## Decision 4 — Google ADK

Chosen as the initial agent orchestration framework.

## Decision 5 — Provider abstraction

Chosen because external job sources differ and can change.

## Decision 6 — Firebase Auth

Chosen for identity/authentication while keeping business data in PostgreSQL.

## Decision 7 — Local embeddings

Chosen to minimize early cost and provider dependency.

## Decision 8 — Human approval

Chosen for resume finalization, outreach, and application submission during the initial product stage.

---

# 51. Important Non-Goals

The HLD does not attempt to define:

- exact database columns
- exact ERD relationships
- exact API schemas
- exact Python classes
- exact Angular component hierarchy
- exact prompt wording
- exact embedding model
- unrestricted scraping implementation
- automatic mass application
- microservice deployment from day one

These are intentionally deferred to later phases.

---

# 52. What We Learned in Phase 2

The important architectural lesson is that the product is not:

```text
Resume → AI → Jobs
```

It is closer to:

```text
Candidate
   ↓
Location
   ↓
Companies
   ↓
Hiring Sources
   ↓
Jobs
   ↓
Candidate Matching
   ↓
Correct Role Profile
   ↓
Tailored Resume
   ↓
Outreach / Application
   ↓
Tracking
```

AI supports reasoning inside this workflow.

It does not replace the application architecture.

---

# 53. HLD Completion Checklist

Before moving to the next phase:

- [x] System context defined
- [x] Major components defined
- [x] Frontend/backend boundary defined
- [x] PostgreSQL role defined
- [x] Qdrant role defined
- [x] Object storage role defined
- [x] Firebase Auth role defined
- [x] Agent architecture defined
- [x] Provider architecture defined
- [x] Company-first discovery flow defined
- [x] Job normalization concept defined
- [x] Matching architecture defined
- [x] Resume tailoring architecture defined
- [x] Human approval boundaries defined
- [x] Background processing defined
- [x] Security boundaries identified
- [x] MVP deployment approach defined
- [x] Scalability direction defined

---

# 54. Transition to Phase 3 — Database / ERD

Phase 2 establishes **what components exist and how they interact**.

The next question is:

> What exact data must the system store, and how are those records related?

Phase 3 will design the PostgreSQL database and ERD.

It will cover:

```text
Candidate
 ├── Candidate Profile
 ├── Role Profiles
 ├── Experiences
 ├── Education
 ├── Projects
 ├── Skills
 └── Resumes

Company
 ├── Locations
 ├── Hiring Sources
 ├── Contacts
 └── Jobs

Job
 ├── Job Sources
 ├── Skills
 ├── Locations
 └── Match Analysis

Application
 ├── Application Events
 ├── Resume
 └── Outreach

Agent
 ├── Agent Runs
 └── Tool Calls
```

The ERD will be designed from this HLD rather than invented independently.

---

# 55. Fixed Phase Sequence

The project documentation sequence remains:

```text
PHASE 0 — Requirements
        ↓
PHASE 1 — Product flows & use cases
        ↓
PHASE 2 — HLD                    ← CURRENTLY COMPLETED
        ↓
PHASE 3 — Database / ERD          ← NEXT
        ↓
PHASE 4 — Backend LLD
        ↓
PHASE 5 — API contracts
        ↓
PHASE 6 — Agent + Tool + MCP architecture
        ↓
PHASE 7 — RAG / Vector architecture
        ↓
PHASE 8 — Security
        ↓
PHASE 9 — Project setup
        ↓
PHASE 10 — Build MVP feature-by-feature
        ↓
PHASE 11 — Testing + evaluation
        ↓
PHASE 12 — Deployment
```

**Phase 2 is complete. Do not start implementation yet. Phase 3 — Database / ERD is the next design step.**
