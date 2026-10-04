# AI Career & Job-Hunting Agent

## Product Requirements & System Architecture

**Document Status:** Draft v1.0\
**Purpose:** Product requirements, architecture, database strategy,
integrations, agent design, and implementation boundaries for the
AI-powered career/job-hunting platform.

------------------------------------------------------------------------

# 1. Product Overview

The product is an AI-assisted career and job-hunting platform designed
to help candidates discover relevant companies and jobs, understand
their fit, prepare truthful job-specific resumes, assist with
outreach/application workflows, and track the complete job-search
lifecycle.

The primary product idea is **not simply an AI resume builder or generic
job matcher**.

The key product direction is:

> **Find the right companies and hiring opportunities around the
> candidate, not just jobs returned by one job portal.**

A candidate can provide a location or area such as **HSR Layout,
Bengaluru**. The system should discover relevant companies in that area,
identify how those companies actually hire, check permitted hiring
sources, find current openings, analyze the job descriptions, match them
against the candidate's verified profile, select the appropriate base
resume, tailor it for the specific role, and assist with
application/outreach.

The platform should eventually support multiple career domains such as:

-   Software Engineering
-   Frontend Engineering
-   Backend Engineering
-   Full Stack Engineering
-   Forward Deployed Engineering
-   Cybersecurity
-   Data/AI
-   Civil Engineering
-   Mechanical Engineering
-   Finance
-   Marketing
-   Other professional domains

IT/software can be the first implementation domain, but the core
architecture must not permanently assume that every candidate is a
software engineer.

------------------------------------------------------------------------

# 2. Product Vision

The system should act as a **career operating system for a candidate**.

It should maintain a structured, truthful representation of the
candidate and use that information across:

1.  Career discovery
2.  Company discovery
3.  Hiring-source discovery
4.  Job discovery
5.  Job-description analysis
6.  Candidate-job matching
7.  Resume/profile selection
8.  Resume tailoring
9.  Skill-gap analysis
10. Outreach generation
11. Application assistance
12. Application tracking
13. Rejection/response analysis
14. Future search improvement

The system must not fabricate candidate experience, skills, education,
projects, employment history, or achievements.

------------------------------------------------------------------------

# 3. Core Product Differentiator

Traditional job-search products commonly begin with:

``` text
Candidate
    ↓
Search jobs
    ↓
Apply
```

This product should support:

``` text
Candidate
    ↓
Location / Career Interests / Preferences
    ↓
Discover Companies
    ↓
Discover How Each Company Hires
    ↓
Check Multiple Permitted Hiring Sources
    ↓
Discover Current Jobs
    ↓
Analyze Job Description
    ↓
Match Candidate
    ↓
Choose Correct Role-Specific Resume
    ↓
Tailor Resume to Specific JD
    ↓
Candidate Approval / Application Rules
    ↓
Apply / Outreach
    ↓
Track Result
    ↓
Learn From Search & Application History
```

------------------------------------------------------------------------

# 4. Product Goals

## 4.1 Primary Goals

The platform should:

-   Maintain a source-of-truth candidate profile.
-   Allow candidates to define career interests and target roles.
-   Allow location-first company discovery.
-   Discover relevant companies around a selected location.
-   Identify the company's official careers page.
-   Identify permitted hiring sources associated with the company.
-   Discover relevant job openings.
-   Normalize jobs from different sources into one internal model.
-   Parse and structure job descriptions.
-   Match jobs against the candidate's verified profile.
-   Select an appropriate role-specific base resume.
-   Tailor resumes for individual job descriptions.
-   Prevent unsupported claims.
-   Generate personalized outreach drafts.
-   Track applications.
-   Track recruiter/company communication where integrations permit.
-   Explain why a job matches or does not match.
-   Identify skill gaps.
-   Improve future searches based on candidate preferences and history.

## 4.2 Secondary Goals

The platform should eventually:

-   Integrate GitHub.
-   Integrate permitted professional-profile data.
-   Integrate email.
-   Support scheduled job discovery.
-   Support controlled application automation.
-   Support interview preparation.
-   Support learning recommendations.
-   Support multiple career domains.
-   Provide analytics about the candidate's job search.

------------------------------------------------------------------------

# 5. Non-Goals for the Initial MVP

The initial version should NOT attempt to:

-   Scrape every website on the internet.
-   Bypass anti-bot systems.
-   Circumvent authentication or access controls.
-   Mass-apply to thousands of jobs without candidate rules.
-   Fabricate candidate experience.
-   Claim that an internally calculated match score is an authoritative
    ATS score.
-   Replace every external job portal.
-   Automatically contact people without appropriate candidate approval.
-   Build every possible integration on day one.

The architecture should support future integrations without making them
mandatory for the MVP.

------------------------------------------------------------------------

# 6. Candidate Source of Truth

A major design principle is:

> **The candidate's master profile is the source of truth.**

A candidate should not have one isolated resume containing everything.

Instead:

``` text
Candidate
   │
   ├── Master Profile
   │      ├── Personal information
   │      ├── Education
   │      ├── Employment
   │      ├── Projects
   │      ├── Skills
   │      ├── Certifications
   │      ├── Achievements
   │      └── Preferences
   │
   ├── Role Profiles
   │      ├── Frontend
   │      ├── Backend
   │      ├── Full Stack
   │      └── FDE
   │
   └── Tailored Resumes
          ├── Job A
          ├── Job B
          └── Job C
```

The master profile stores verified facts.

Role profiles organize those facts for a particular career direction.

A tailored resume may:

-   reorder information,
-   change emphasis,
-   select relevant projects,
-   adjust wording,
-   highlight relevant skills,
-   reorganize sections,

but must not invent unsupported facts.

------------------------------------------------------------------------

# 7. Functional Requirements

## FR-001 Candidate Registration

The system shall allow a candidate to create an account.

Authentication may initially use Firebase Authentication.

The application backend should verify the Firebase identity token and
map it to an internal candidate record.

------------------------------------------------------------------------

## FR-002 Candidate Profile

The system shall allow a candidate to maintain:

-   Name
-   Contact information
-   Location
-   Education
-   Employment history
-   Projects
-   Skills
-   Certifications
-   Achievements
-   Languages
-   Career interests
-   Target roles
-   Target industries
-   Target locations
-   Salary preferences
-   Work-mode preferences
-   Experience level

------------------------------------------------------------------------

## FR-003 Resume Upload

The system shall allow candidates to upload existing resumes.

Supported initial format:

-   PDF
-   DOCX

The system should extract structured information from the resume.

Original files should remain stored separately from structured candidate
data.

------------------------------------------------------------------------

## FR-004 Resume Parsing

The system should extract:

-   Summary
-   Skills
-   Employment
-   Projects
-   Education
-   Certifications
-   Achievements
-   Keywords
-   Technologies
-   Job titles
-   Years of experience

Extracted information must be treated as candidate data requiring
validation where appropriate.

------------------------------------------------------------------------

## FR-005 Role Profiles

A candidate should be able to maintain multiple role-specific profiles.

Example:

``` text
Candidate
   ├── Full Stack Profile
   ├── Frontend Profile
   ├── FDE Profile
   └── Backend Profile
```

This prevents the system from using the same resume for every job.

------------------------------------------------------------------------

## FR-006 Location-First Discovery

The candidate should be able to specify:

-   City
-   Area/neighborhood
-   Radius
-   Remote preference
-   Hybrid preference
-   On-site preference

Example:

``` text
Location:
HSR Layout, Bengaluru

Radius:
10 km
```

The system should then discover relevant companies using permitted data
sources.

------------------------------------------------------------------------

## FR-007 Company Discovery

The system should discover companies relevant to the selected location
and career interests.

For every discovered company, the system should attempt to maintain:

-   Company name
-   Website
-   Official domain
-   Location
-   Industry
-   Company size where available
-   Careers URL
-   Hiring sources
-   Source confidence
-   Last verified time

------------------------------------------------------------------------

# 8. Hiring Source Intelligence

A company may hire through multiple channels.

Example:

``` text
Company A
│
├── Official Careers Page
├── LinkedIn
├── Naukri
├── Indeed
├── Wellfound
└── Other permitted source
```

The system should not assume that every company uses every portal.

Instead, the system should store a relationship between:

``` text
Company
    ↕
Hiring Source
    ↕
Observed Job
```

This allows the platform to learn which sources are useful for each
company.

Example:

``` text
Company X
Official Careers → Active
LinkedIn → Active
Naukri → Frequently used
Indeed → Rarely used
```

The data should include timestamps because hiring-source information can
become stale.

------------------------------------------------------------------------

# 9. Job Discovery

The platform should discover jobs through supported/permitted providers.

Potential providers include:

-   Company career pages
-   Official job APIs
-   Permitted third-party job APIs
-   User-provided job URLs
-   Supported integrations
-   Other legally/permissibly accessible sources

The system should normalize all discovered jobs into an internal `Job`
model.

------------------------------------------------------------------------

# 10. Job Normalization

Different sources may describe the same job differently.

The internal job model should normalize:

-   Job title
-   Company
-   Location
-   Work mode
-   Employment type
-   Experience requirements
-   Education requirements
-   Skills
-   Responsibilities
-   Qualifications
-   Salary where available
-   Source
-   Source URL
-   External job ID
-   Posted date
-   Last observed date
-   Application URL
-   Job status

The original source information should be preserved.

------------------------------------------------------------------------

# 11. Duplicate Job Detection

The same job may appear on:

``` text
Company Careers
LinkedIn
Naukri
Indeed
```

The system should attempt to identify duplicates using:

-   Company
-   External job ID
-   Normalized title
-   Location
-   Similar description
-   Application URL
-   Semantic similarity
-   Posting timestamps

The system should maintain one canonical internal job where appropriate
while retaining source records.

------------------------------------------------------------------------

# 12. Job Description Analysis

For every relevant job, the system should extract:

### Required skills

Example:

``` text
Python
FastAPI
REST APIs
SQL
Docker
AWS
```

### Preferred skills

Example:

``` text
Kubernetes
Redis
Terraform
```

### Responsibilities

Example:

``` text
Build APIs
Debug production issues
Collaborate with frontend engineers
Deploy services
```

### Eligibility

Example:

``` text
Experience: 1–3 years
Location: Bengaluru
Education: Bachelor's degree
```

------------------------------------------------------------------------

# 13. Candidate-Job Matching

Matching should not be represented as a fake universal ATS score.

The system should provide structured evidence.

Example:

``` text
Job:
Full Stack Engineer

Strong matches:
✓ Angular
✓ TypeScript
✓ FastAPI
✓ MySQL
✓ Docker

Partial matches:
△ AWS
△ React

Missing / not verified:
? Kubernetes

Experience:
✓ 1–3 years requirement appears compatible

Evidence:
- Angular appears in candidate project X
- FastAPI appears in project Y
```

The system should distinguish:

-   Strong match
-   Partial match
-   Missing
-   Not verified
-   Eligibility issue

------------------------------------------------------------------------

# 14. Resume Selection

The system should select the appropriate role-specific resume before
tailoring.

Example:

``` text
Job
 ↓
Job Classification
 ↓
Frontend role?
 ↓
Use Frontend Resume/Profile
```

Another job:

``` text
Job
 ↓
FDE role
 ↓
Use FDE Resume/Profile
```

The system should not automatically use one universal resume.

------------------------------------------------------------------------

# 15. Resume Tailoring

Resume tailoring may:

-   Reorder skills
-   Reorder projects
-   Rephrase truthful experience
-   Highlight relevant achievements
-   Adjust summary
-   Select relevant projects
-   Align terminology with the JD
-   Improve keyword coverage

It must not:

-   Invent technologies
-   Invent years of experience
-   Invent projects
-   Invent achievements
-   Claim unverified certifications
-   Claim employment at a company where the candidate did not work

A validation step should compare generated resume claims against the
candidate source of truth.

------------------------------------------------------------------------

# 16. Outreach

The system should generate personalized outreach for:

-   Recruiters
-   HR
-   Hiring managers
-   Founders
-   Company contact addresses

The correct outreach target depends on company size and available
public/permitted information.

Initial implementation should require candidate approval before sending.

------------------------------------------------------------------------

# 17. Application Assistance

The application workflow should support:

``` text
Discovered
   ↓
Reviewed
   ↓
Matched
   ↓
Resume Prepared
   ↓
Candidate Approved
   ↓
Applied
   ↓
Follow-up
   ↓
Interview
   ↓
Offer / Rejected / Withdrawn
```

The initial system should prioritize assisted applications.

Controlled automation may be added later using:

-   Official APIs
-   Permitted integrations
-   Candidate-defined rules
-   Human approval

------------------------------------------------------------------------

# 18. Application Tracking

The system should track:

-   Job
-   Company
-   Resume version
-   Application date
-   Application source
-   Application URL
-   Status
-   Recruiter
-   Outreach
-   Follow-up dates
-   Interview stages
-   Rejection
-   Offer
-   Notes

------------------------------------------------------------------------

# 19. Chatbot Requirements

The chatbot should be a career-system interface, not a generic chatbot.

Examples:

``` text
"Find frontend jobs around HSR."

"Which companies near me hire FDEs?"

"Why did you reject this job?"

"Create a resume for this job."

"What skills am I missing?"

"Show companies where my profile has strong fit."

"Track my application to Company X."
```

The chatbot should call application tools/agents instead of answering
purely from an LLM's general knowledge.

------------------------------------------------------------------------

# 20. Agent Architecture

Google ADK should be used as the agent orchestration framework.

Initial architecture:

``` text
Career Orchestrator
│
├── Candidate Agent
├── Company Agent
├── Job Discovery Agent
├── Matching Agent
├── Resume Agent
└── Application Agent
```

Additional agents should be introduced only when the domain complexity
justifies them.

Potential future agents:

``` text
Location Intelligence Agent
Hiring Source Intelligence Agent
Skill Intelligence Agent
Outreach Agent
Email Tracking Agent
Interview Agent
Learning Agent
```

------------------------------------------------------------------------

# 21. Agent Responsibilities

## Candidate Agent

Responsible for:

-   Candidate profile
-   Career preferences
-   Skills
-   Experience
-   Role profiles
-   Candidate evidence

## Company Agent

Responsible for:

-   Company discovery
-   Company enrichment
-   Careers pages
-   Hiring-source relationships
-   Company research

## Job Discovery Agent

Responsible for:

-   Searching supported sources
-   Fetching job data
-   Normalization
-   Deduplication
-   Job freshness

## Matching Agent

Responsible for:

-   JD analysis
-   Skill comparison
-   Eligibility checks
-   Evidence retrieval
-   Match explanation

## Resume Agent

Responsible for:

-   Resume selection
-   Tailoring
-   Claim validation
-   Resume generation

## Application Agent

Responsible for:

-   Application preparation
-   Application tracking
-   Outreach drafts
-   Follow-up workflows

------------------------------------------------------------------------

# 22. Tool Layer

Agents should not directly contain every external integration.

Instead:

``` text
Agent
  ↓
Tool Interface
  ↓
Provider / Service
  ↓
External System
```

Example:

``` text
Job Discovery Agent
       ↓
   JobSearchTool
       ↓
   JobSourceProvider
       ↓
   LinkedIn / Company API / Other permitted source
```

This keeps the agent layer independent from external providers.

------------------------------------------------------------------------

# 23. Provider Architecture for Job Sources

A provider interface should conceptually support:

``` text
JobSourceProvider
├── search_jobs()
├── get_job()
├── normalize_job()
└── health_check()
```

Potential implementations:

``` text
CompanyCareerProvider
PermittedJobAPIProvider
UserProvidedJobProvider
LinkedInProvider
NaukriProvider
IndeedProvider
WellfoundProvider
```

The exact provider implementation depends on available official APIs,
permitted access, licensing, and integration availability.

The architecture must not assume unrestricted scraping.

------------------------------------------------------------------------

# 24. MCP Architecture

MCP should be treated as an integration protocol/tool interface rather
than the application's primary architecture.

Potential MCP tools:

``` text
GitHub MCP
Email MCP
Career Data MCP
Company Research MCP
Internal Career Tools MCP
```

Google ADK can consume MCP tools where appropriate.

Example:

``` text
ADK Agent
   ↓
MCP Toolset
   ↓
Tool
   ↓
External Service
```

MCP should be used when it provides a meaningful integration boundary.
Internal application services do not need to become MCP servers merely
for architectural decoration.

------------------------------------------------------------------------

# 25. GitHub Integration

GitHub integration should be optional.

With candidate authorization, the system may retrieve permitted
information such as:

-   Repositories
-   README files
-   Languages
-   Project descriptions
-   Commit/activity signals where appropriate
-   Public project metadata

The system should use GitHub information as evidence rather than
automatically claiming every repository is professional experience.

------------------------------------------------------------------------

# 26. LinkedIn Integration

The system must not assume unrestricted access to LinkedIn data.

Possible approaches:

-   Official API/integration where available
-   User-provided profile information
-   User-provided exported data
-   Supported third-party integration

The architecture should keep LinkedIn behind a provider interface.

------------------------------------------------------------------------

# 27. Database Strategy

## 27.1 Primary Recommendation

The primary application database should be:

> **PostgreSQL**

Reason: this product has a highly relational domain.

Important relationships include:

``` text
Candidate
  ↓
Candidate Profiles
  ↓
Role Profiles
  ↓
Resumes
  ↓
Tailored Resumes

Company
  ↓
Hiring Sources
  ↓
Jobs
  ↓
Applications
  ↓
Outreach / Interviews

Candidate
  ↓
Skills
  ↓
Evidence
  ↓
Job Skill Requirements
```

These relationships are central to the product.

------------------------------------------------------------------------

# 28. SQL vs NoSQL Decision

## PostgreSQL

Use PostgreSQL for:

-   Candidates
-   Candidate profiles
-   Role profiles
-   Employment
-   Education
-   Projects
-   Skills
-   Companies
-   Locations
-   Hiring sources
-   Jobs
-   Job requirements
-   Applications
-   Outreach
-   Interviews
-   Resume metadata
-   Integrations
-   Preferences
-   Search history
-   Audit records

Advantages:

-   Strong relationships
-   Foreign keys
-   Transactions
-   Constraints
-   Unique indexes
-   Complex queries
-   Aggregations
-   Reliable consistency
-   Mature ecosystem
-   Easy reporting
-   Industry-standard relational modeling

------------------------------------------------------------------------

## Firestore

Firestore can still be useful for selected Firebase functionality, but
it should not be the primary source of truth for the complex career
domain if PostgreSQL is chosen.

Firebase Authentication can remain the authentication layer.

Example:

``` text
Firebase Auth
      ↓
Identity Token
      ↓
FastAPI
      ↓
PostgreSQL Candidate
```

The Firebase UID can be stored as an external identity identifier in
PostgreSQL.

------------------------------------------------------------------------

# 29. Why Not Make Firestore the Main Database?

Firestore is excellent for document-oriented applications, but this
product has many relationships and cross-entity queries.

For example:

``` text
Find companies
near a location
that hire for a role
that have active jobs
requiring skills
that match a candidate
and have not already been applied to
and rank by candidate preferences.
```

This type of relational querying becomes much more natural in
PostgreSQL.

Firestore can still be introduced later for a specific use case if
needed.

------------------------------------------------------------------------

# 30. SQL Database Logical Model

Core entities:

``` text
users
candidates
candidate_profiles
role_profiles
experiences
education
projects
skills
candidate_skills
skill_evidence

companies
company_locations
hiring_sources
company_hiring_sources

jobs
job_sources
job_skills
job_locations

resumes
resume_versions
tailored_resumes

applications
application_events

outreach
contacts

integrations
search_runs
agent_runs

preferences
notifications
audit_logs
```

------------------------------------------------------------------------

# 31. Candidate Relationships

Conceptually:

``` text
Candidate
  │
  ├── 1:N CandidateProfiles
  │
  ├── 1:N RoleProfiles
  │
  ├── 1:N Experiences
  │
  ├── 1:N Education
  │
  ├── 1:N Projects
  │
  ├── N:M Skills
  │
  ├── 1:N Resumes
  │
  └── 1:N Applications
```

------------------------------------------------------------------------

# 32. Company Relationships

``` text
Company
  │
  ├── 1:N CompanyLocations
  │
  ├── 1:N Jobs
  │
  ├── N:M HiringSources
  │
  └── 1:N Contacts
```

The company-to-hiring-source relationship should be represented
explicitly.

Example:

``` text
Company: ExampleTech

Hiring Source:
LinkedIn

Relationship:
Observed active hiring source

Last verified:
2026-10-01
```

------------------------------------------------------------------------

# 33. Job Relationships

A job belongs to a company but can have multiple source representations.

Conceptually:

``` text
Company
   ↓
Canonical Job
   ↓
Job Sources
   ├── Company Careers
   ├── LinkedIn
   └── Other Source
```

This allows duplicate jobs to be consolidated while preserving source
history.

------------------------------------------------------------------------

# 34. Candidate ↔ Job Relationship

The candidate and job relationship is not stored only as a simple score.

It should support:

``` text
Candidate
   ↕
Match Analysis
   ↕
Job
```

Match analysis may include:

-   Match status
-   Skill matches
-   Partial matches
-   Missing skills
-   Eligibility
-   Evidence
-   Generated explanation
-   Match version
-   Analysis timestamp

------------------------------------------------------------------------

# 35. Application Relationship

An application should connect:

``` text
Candidate
   ↓
Application
   ├── Job
   ├── Company
   ├── Resume Version
   ├── Source
   ├── Status
   ├── Outreach
   └── Application Events
```

This gives a complete history.

------------------------------------------------------------------------

# 36. Skill Intelligence

Skills should be first-class entities.

Example:

``` text
Skill
FastAPI

Aliases:
Fast API

Category:
Backend Framework

Related:
Python
REST
Pydantic
ASGI
```

The skill system should eventually support:

-   Canonical skill
-   Aliases
-   Categories
-   Related skills
-   Prerequisites
-   Evidence
-   Candidate proficiency
-   Job demand
-   Domain
-   Role relevance

------------------------------------------------------------------------

# 37. RAG and Vector Database

Vector search should not replace PostgreSQL.

Use a hybrid architecture:

``` text
                ┌───────────────┐
                │ PostgreSQL    │
                │ Structured DB │
                └───────┬───────┘
                        │
                        │
                ┌───────▼───────┐
                │ Retrieval     │
                │ Service       │
                └───────┬───────┘
                        │
                ┌───────▼───────┐
                │ Qdrant        │
                │ Vector DB     │
                └───────────────┘
```

PostgreSQL answers:

``` text
Which jobs are active?
Which companies are in Bengaluru?
Has the candidate already applied?
What skills does the candidate have?
```

Qdrant answers:

``` text
Which projects are semantically similar to this JD?
Which candidate evidence is relevant?
Which jobs are semantically similar?
```

------------------------------------------------------------------------

# 38. Data Storage Responsibilities

## PostgreSQL

Source of truth for structured business data.

## Qdrant

Semantic/vector representations.

## Object Storage

Original files and generated documents.

Potential options:

-   Firebase Storage
-   S3-compatible storage
-   AWS S3 later

Examples:

``` text
candidate/resumes/original.pdf
candidate/resumes/tailored/job-123.pdf
candidate/documents/cover-letter-job-123.pdf
```

------------------------------------------------------------------------

# 39. Recommended MVP Database

For local development:

``` text
PostgreSQL
    +
Qdrant
    +
Local filesystem / Firebase Storage
```

For authentication:

``` text
Firebase Authentication
```

This keeps the system affordable while using a database model
appropriate for production.

------------------------------------------------------------------------

# 40. PostgreSQL Initial Schema Concept

A simplified conceptual schema:

``` text
candidates
-----------
id PK
firebase_uid UNIQUE
name
email
created_at
updated_at


companies
---------
id PK
name
domain
website
industry
company_size
created_at
updated_at


hiring_sources
--------------
id PK
name
type
base_url


company_hiring_sources
----------------------
id PK
company_id FK
hiring_source_id FK
status
last_verified_at


jobs
----
id PK
company_id FK
title
description
employment_type
work_mode
status
posted_at
last_seen_at
canonical_url
created_at


job_sources
-----------
id PK
job_id FK
hiring_source_id FK
external_job_id
source_url
first_seen_at
last_seen_at


skills
------
id PK
name
category
canonical_name


job_skills
----------
job_id FK
skill_id FK
requirement_type


candidate_skills
----------------
candidate_id FK
skill_id FK
proficiency
verification_status


resumes
-------
id PK
candidate_id FK
role_profile_id FK
file_path
resume_type
created_at


applications
------------
id PK
candidate_id FK
job_id FK
resume_id FK
status
applied_at
created_at
updated_at
```

This is only the starting conceptual schema. The exact physical schema
should be finalized during LLD.

------------------------------------------------------------------------

# 41. Database Constraints

The database should enforce important rules.

Examples:

``` text
firebase_uid UNIQUE

company domain UNIQUE where appropriate

job source + external job ID UNIQUE

candidate + job application UNIQUE where appropriate

foreign keys enabled

timestamps required

status values constrained

created_at / updated_at maintained
```

Business rules should not rely entirely on the LLM.

------------------------------------------------------------------------

# 42. Data Consistency

Critical operations should use database transactions.

Example:

``` text
Create Application
    ↓
Verify Candidate
    ↓
Verify Job
    ↓
Verify Resume
    ↓
Create Application
    ↓
Create Application Event
    ↓
Commit
```

If one critical operation fails, the transaction should roll back.

------------------------------------------------------------------------

# 43. Search Architecture

Search should use multiple strategies.

``` text
Candidate Query
      │
      ├── Structured SQL filtering
      │
      ├── Full-text search
      │
      └── Semantic/vector search
```

Example:

``` text
"Frontend jobs near HSR with Angular"
```

Structured filters:

``` text
location = HSR
role = Frontend
skill = Angular
```

Semantic search:

``` text
Find jobs whose responsibilities are similar to the candidate's experience.
```

------------------------------------------------------------------------

# 44. Location Architecture

Location should be structured rather than stored only as text.

Potential model:

``` text
Country
  ↓
State
  ↓
City
  ↓
Area / Neighborhood
  ↓
Coordinates where permitted
```

The system should support:

-   City search
-   Area search
-   Radius search
-   Remote
-   Hybrid
-   On-site

A future implementation may use PostgreSQL/PostGIS if geographic queries
become important.

------------------------------------------------------------------------

# 45. Application Architecture

``` text
Angular Web App
        │
        │ HTTPS
        ▼
FastAPI
        │
        ├── Authentication
        ├── REST APIs
        ├── Business Services
        ├── Agent Services
        ├── Retrieval
        └── Integration Layer
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
 PostgreSQL         Qdrant       Object Storage
        │
        ▼
 Structured         Semantic       Files
 Data               Search
```

------------------------------------------------------------------------

# 46. Backend Layering

FastAPI should be organized into layers.

``` text
API / Routes
     ↓
Application Services
     ↓
Domain Logic
     ↓
Repositories
     ↓
PostgreSQL
```

External integrations should be separate:

``` text
Application Service
     ↓
Provider Interface
     ↓
Provider Implementation
```

This prevents API routes from becoming large blocks of business logic.

------------------------------------------------------------------------

# 47. Recommended Backend Structure

``` text
apps/api/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── candidates.py
│   │       ├── profiles.py
│   │       ├── jobs.py
│   │       ├── companies.py
│   │       ├── resumes.py
│   │       ├── matching.py
│   │       ├── applications.py
│   │       ├── agents.py
│   │       └── chat.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── providers/
│   └── integrations/
│
├── tests/
├── alembic/
└── pyproject.toml
```

------------------------------------------------------------------------

# 48. Frontend Architecture

Angular should use feature-based organization.

``` text
apps/web/
└── src/app/
    ├── core/
    │   ├── auth/
    │   ├── guards/
    │   ├── interceptors/
    │   └── services/
    │
    ├── shared/
    │   ├── components/
    │   ├── pipes/
    │   └── directives/
    │
    └── features/
        ├── onboarding/
        ├── dashboard/
        ├── jobs/
        ├── companies/
        ├── resumes/
        ├── applications/
        ├── profile/
        └── chat/
```

------------------------------------------------------------------------

# 49. REST API Design

Initial API groups:

``` text
/api/v1/auth
/api/v1/candidates
/api/v1/profiles
/api/v1/resumes
/api/v1/jobs
/api/v1/companies
/api/v1/search
/api/v1/matching
/api/v1/applications
/api/v1/agents
/api/v1/chat
/api/v1/integrations
```

Examples:

``` text
GET  /api/v1/candidates/profile

POST /api/v1/jobs/analyze

POST /api/v1/jobs/match

POST /api/v1/resumes/tailor

POST /api/v1/agents/job-hunt

POST /api/v1/chat

GET  /api/v1/companies

GET  /api/v1/jobs

POST /api/v1/applications
```

------------------------------------------------------------------------

# 50. Authentication Flow

Initial flow:

``` text
Angular
   ↓
Firebase Authentication
   ↓
Firebase ID Token
   ↓
FastAPI Authorization Header
   ↓
Firebase Token Verification
   ↓
firebase_uid
   ↓
PostgreSQL Candidate
```

Firebase Authentication handles identity.

PostgreSQL handles application-domain data.

------------------------------------------------------------------------

# 51. Security Requirements

The system should implement:

-   Authentication
-   Authorization
-   Role-based access where needed
-   Input validation
-   Secure secret storage
-   Token validation
-   Rate limiting
-   Audit logging
-   File validation
-   Safe document processing
-   Provider credential isolation
-   Least-privilege integrations
-   Candidate approval for sensitive actions

The LLM must never be treated as a security boundary.

------------------------------------------------------------------------

# 52. Agent Security

Agents should have limited tools.

For example:

``` text
Matching Agent
    ✓ read candidate profile
    ✓ read job
    ✓ retrieve evidence
    ✗ send email
    ✗ submit application
```

Application Agent may have:

``` text
✓ read job
✓ read candidate
✓ prepare application
✓ create draft

Requires approval:
→ submit application
→ send outreach
```

Tool permissions should be explicit.

------------------------------------------------------------------------

# 53. Human-in-the-Loop

Sensitive actions should initially require approval.

Examples:

``` text
Generate resume
      ↓
Candidate reviews
      ↓
Approve

Generate outreach
      ↓
Candidate reviews
      ↓
Approve

Submit application
      ↓
Candidate confirms
      ↓
Submit
```

Later, users may define trusted automation rules.

------------------------------------------------------------------------

# 54. Job Source Freshness

Job data becomes stale quickly.

Every source record should therefore maintain:

``` text
first_seen_at
last_seen_at
last_verified_at
source_status
```

Jobs can then be classified as:

``` text
Active
Recently Seen
Possibly Stale
Expired
Closed
```

The system should avoid presenting old jobs as newly discovered.

------------------------------------------------------------------------

# 55. Agent Observability

Every significant agent execution should have traceable information.

Example:

``` text
Agent Run
---------
id
candidate_id
agent_type
started_at
completed_at
status
input_reference
output_reference
tool_calls
error
model
token/cost metadata where available
```

This helps debug AI behavior.

------------------------------------------------------------------------

# 56. AI Evaluation

The system should evaluate:

### Matching

-   Correct skill extraction
-   Correct evidence
-   False positive rate
-   False negative rate

### Resume

-   Claim accuracy
-   JD relevance
-   Formatting
-   Keyword coverage
-   Unsupported claim detection

### Job Discovery

-   Duplicate rate
-   Freshness
-   Relevance
-   Source reliability

### Agent

-   Tool correctness
-   Hallucination rate
-   Failure recovery
-   Latency

------------------------------------------------------------------------

# 57. AI Provider Abstraction

The system should not hard-code the entire application around one model
provider.

Use a model interface:

``` text
LLM Provider
   ├── Gemini
   ├── OpenAI
   ├── Local Model
   └── Future Provider
```

Initial development can use Gemini.

Future providers can be added without rewriting the domain layer.

------------------------------------------------------------------------

# 58. Cost-Conscious Development

Initial development should prioritize free/local infrastructure.

Recommended:

``` text
Angular
FastAPI
PostgreSQL locally
Qdrant locally
Firebase Auth
Firebase Storage if needed
Gemini API within available quota
Hugging Face embedding model locally
Docker
Git/GitHub
```

Avoid unnecessary paid infrastructure during MVP development.

------------------------------------------------------------------------

# 59. Local Development

Recommended local environment:

``` text
Docker Compose
│
├── PostgreSQL
└── Qdrant

Local Python
└── FastAPI

Local Node
└── Angular
```

Optional:

``` text
Firebase
└── Authentication
```

------------------------------------------------------------------------

# 60. Production Evolution

A future production architecture could become:

``` text
CDN / Web
    ↓
Angular Application
    ↓
API Gateway / Load Balancer
    ↓
FastAPI Services
    ↓
PostgreSQL
    ↓
Redis / Queue
    ↓
Agent Workers
    ↓
External Providers

Qdrant / Vector Infrastructure
Object Storage
Observability
```

The MVP should not start with microservices.

------------------------------------------------------------------------

# 61. Monolith First

Initial backend should be a modular monolith.

``` text
FastAPI
│
├── Candidate Module
├── Company Module
├── Job Module
├── Matching Module
├── Resume Module
├── Application Module
└── Agent Module
```

This provides clear boundaries without operational complexity.

Services can be extracted later if necessary.

------------------------------------------------------------------------

# 62. Project Repository Structure

``` text
career-agent/
│
├── apps/
│   ├── web/
│   └── api/
│
├── agents/
│   ├── career/
│   ├── candidate/
│   ├── jobs/
│   ├── company/
│   ├── resume/
│   └── matching/
│
├── tools/
│   ├── search/
│   ├── jobs/
│   ├── companies/
│   ├── resume/
│   ├── github/
│   ├── email/
│   └── location/
│
├── mcp/
│
├── packages/
│   ├── schemas/
│   ├── models/
│   ├── retrieval/
│   ├── embeddings/
│   └── shared/
│
├── data/
│   ├── seed/
│   └── evaluation/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
│
├── docs/
│   ├── requirements/
│   ├── architecture/
│   ├── api/
│   ├── agents/
│   ├── integrations/
│   └── decisions/
│
├── scripts/
├── docker-compose.yml
├── .env.example
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

Not every folder should be created on Day 1. The repository should
evolve with the requirements.

------------------------------------------------------------------------

# 63. Documentation Structure

``` text
docs/
├── requirements/
│   ├── req.md
│   ├── user-stories.md
│   └── acceptance-criteria.md
│
├── architecture/
│   ├── hld.md
│   ├── lld.md
│   ├── system-context.md
│   ├── data-flow.md
│   ├── database.md
│   └── architecture-decisions.md
│
├── api/
│   └── api-contract.md
│
├── agents/
│   ├── agent-architecture.md
│   ├── agent-responsibilities.md
│   ├── tool-registry.md
│   └── evaluation.md
│
└── integrations/
    ├── job-sources.md
    ├── github.md
    └── email.md
```

------------------------------------------------------------------------

# 64. Major Data Flow

``` text
Candidate
   ↓
Onboarding
   ↓
Master Profile
   ↓
Role Preferences
   ↓
Location Preferences
   ↓
Company Discovery
   ↓
Hiring Source Discovery
   ↓
Job Discovery
   ↓
Job Normalization
   ↓
JD Analysis
   ↓
Candidate Retrieval
   ↓
Match Analysis
   ↓
Resume Selection
   ↓
Resume Tailoring
   ↓
Claim Validation
   ↓
Candidate Approval
   ↓
Application / Outreach
   ↓
Application Tracking
   ↓
Analytics / Feedback
```

------------------------------------------------------------------------

# 65. Example End-to-End Scenario

Candidate:

``` text
Role:
Full Stack / FDE

Location:
HSR Layout, Bengaluru

Skills:
Angular
TypeScript
FastAPI
Python
MySQL
Docker
AWS
Firebase
```

The system:

``` text
1. Finds companies around HSR.

2. Filters companies according to the candidate's career interests.

3. Finds official websites.

4. Finds careers pages.

5. Determines which permitted hiring sources are associated
   with each company.

6. Finds current jobs.

7. Normalizes jobs.

8. Removes duplicates.

9. Extracts requirements.

10. Compares requirements with the candidate profile.

11. Retrieves relevant candidate evidence.

12. Selects Full Stack or FDE role profile.

13. Tailors the appropriate resume.

14. Validates claims.

15. Shows the candidate the result.

16. Candidate approves application/outreach.

17. System records the application.

18. Future responses are tracked.
```

------------------------------------------------------------------------

# 66. Important Architectural Principle

The LLM is not the database.

The LLM is not the source of truth.

The LLM is not the authorization system.

The LLM is not the application state.

Instead:

``` text
PostgreSQL
    = business truth

Qdrant
    = semantic retrieval

Object Storage
    = files

Firebase Auth
    = identity

FastAPI
    = application/business API

Google ADK
    = agent orchestration

MCP / Providers
    = integration/tool boundary

Gemini / Other Models
    = reasoning and generation
```

This separation is critical.

------------------------------------------------------------------------

# 67. Initial MVP Scope

The first usable MVP should contain:

### Phase 1

-   Firebase authentication
-   Candidate onboarding
-   Master profile
-   Resume upload
-   Resume parsing
-   PostgreSQL
-   Basic skill model
-   Role profiles

### Phase 2

-   Company discovery
-   Location filtering
-   Company records
-   Hiring-source model
-   Initial permitted job source
-   Job normalization

### Phase 3

-   JD analysis
-   Candidate-job matching
-   Evidence retrieval
-   Qdrant/RAG

### Phase 4

-   Resume selection
-   Resume tailoring
-   Claim validation
-   PDF/DOCX generation

### Phase 5

-   Application tracking
-   Outreach generation
-   Chat interface

### Phase 6

-   Additional providers
-   GitHub integration
-   Email integration
-   Scheduled searches
-   Hiring-source intelligence

### Phase 7

-   Controlled application automation
-   Advanced analytics
-   Multi-domain career support

------------------------------------------------------------------------

# 68. Development Method

The project should be built as a learning project as well as a product.

For every major feature:

``` text
1. Understand the problem
2. Learn the concept
3. Define requirements
4. Design HLD
5. Design LLD
6. Design database
7. Define API contract
8. Implement
9. Run locally
10. Test
11. Debug
12. Explain the implementation
13. Document decisions
14. Prepare interview questions
```

AI coding tools such as Codex should assist implementation, but
architectural decisions should remain understandable by the developer.

------------------------------------------------------------------------

# 69. Coding Principles

The implementation should prioritize:

-   Readability
-   Strong typing
-   Small functions
-   Clear module boundaries
-   Dependency injection where useful
-   Repository pattern where appropriate
-   Provider interfaces
-   Pydantic schemas
-   Database migrations
-   Automated tests
-   Structured logging
-   Error handling
-   Security
-   Documentation

Avoid premature abstractions.

------------------------------------------------------------------------

# 70. Architectural Decisions

## ADR-001: PostgreSQL as Primary Database

**Decision:** Use PostgreSQL as the primary application database.

**Reason:** The domain has many strong relationships, constraints,
transactional workflows, and reporting requirements.

------------------------------------------------------------------------

## ADR-002: Firebase Authentication

**Decision:** Use Firebase Authentication initially.

**Reason:** It provides a practical authentication solution while
PostgreSQL remains the application data source of truth.

------------------------------------------------------------------------

## ADR-003: Qdrant for Semantic Retrieval

**Decision:** Use Qdrant for vector search.

**Reason:** Semantic candidate/job/evidence retrieval is useful, while
structured business data remains in PostgreSQL.

------------------------------------------------------------------------

## ADR-004: Modular Monolith First

**Decision:** Start with one FastAPI backend organized into clear
modules.

**Reason:** This keeps development and deployment simple while
preserving boundaries for future extraction.

------------------------------------------------------------------------

## ADR-005: Provider-Based Job Sources

**Decision:** External job sources must be accessed through provider
interfaces.

**Reason:** Job portals and APIs differ in capabilities, access rules,
data formats, and availability.

------------------------------------------------------------------------

## ADR-006: Master Profile + Role Profiles

**Decision:** Maintain a source-of-truth candidate profile plus
role-specific profiles.

**Reason:** One resume should not be forced to represent every job
target.

------------------------------------------------------------------------

## ADR-007: Human Approval for Sensitive Actions

**Decision:** Applications and outbound communication require candidate
approval in the initial versions.

**Reason:** The candidate remains in control and the system reduces
accidental submissions or incorrect communication.

------------------------------------------------------------------------

# 71. Future Scalability

When the product grows, potential additions include:

-   PostgreSQL read replicas
-   Redis
-   Background workers
-   Message queues
-   Dedicated agent workers
-   Search infrastructure
-   PostGIS
-   Dedicated object storage
-   Observability stack
-   Provider health monitoring
-   Rate-limit management
-   Job freshness pipelines
-   Event-driven application tracking

These should be introduced based on actual system requirements rather
than prematurely.

------------------------------------------------------------------------

# 72. Final Architecture Summary

``` text
                         ┌──────────────────────┐
                         │    Angular Web App   │
                         │ Dashboard / Jobs /   │
                         │ Resume / Chat / Apps │
                         └──────────┬───────────┘
                                    │
                                  HTTPS
                                    │
                         ┌──────────▼───────────┐
                         │       FastAPI        │
                         │ REST / Auth / API    │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼──────────────────┐
                  │                 │                  │
                  ▼                 ▼                  ▼
           ┌────────────┐   ┌──────────────┐   ┌──────────────┐
           │ PostgreSQL │   │ Google ADK   │   │ Retrieval    │
           │ Business   │   │ Agents       │   │ Service      │
           │ Data       │   │              │   └──────┬───────┘
           └────────────┘   └──────┬───────┘          │
                                   │                  ▼
                            ┌──────▼──────┐      ┌──────────┐
                            │ Tools / MCP │      │ Qdrant   │
                            └──────┬──────┘      └──────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
                  ▼                ▼                ▼
           Job Providers    Company Sources   User Integrations
                  │                │                │
                  └────────────────┼────────────────┘
                                   │
                            External Services

                         ┌────────────────────┐
                         │ Object Storage     │
                         │ Resumes / Docs     │
                         └────────────────────┘

                         ┌────────────────────┐
                         │ Firebase Auth      │
                         │ Identity           │
                         └────────────────────┘
```

------------------------------------------------------------------------

# 73. Key Decision for the Project

The most important architectural decision at this stage is:

> **Use PostgreSQL as the system-of-record relational database, Qdrant
> as the semantic retrieval database, object storage for files, Firebase
> Authentication for identity, FastAPI for application APIs, and Google
> ADK/MCP/provider interfaces for agentic integrations.**

This gives the product a strong relational foundation while still
supporting AI, RAG, multiple job portals, company discovery, and future
automation.

The architecture should be built around **companies, hiring sources,
jobs, candidates, skills, resumes, and applications as first-class
entities**, rather than around a single "job search" table or a generic
chatbot.

------------------------------------------------------------------------

# 74. Next Design Documents

After this requirements document, the next documents should be created
in this order:

``` text
01. Requirements
        ↓
02. HLD
        ↓
03. Database ERD + Database LLD
        ↓
04. API Contract
        ↓
05. Agent Architecture
        ↓
06. Tool / Provider Architecture
        ↓
07. RAG Architecture
        ↓
08. Security Design
        ↓
09. Frontend Architecture
        ↓
10. Implementation Plan
```

Only after these foundations are sufficiently clear should major
application coding begin.
