Phase 10.6 — Candidate Profile
1. Purpose

Phase 10.6 expands the basic candidate onboarding created in Phase 10.5 into the application's complete candidate professional profile.

The candidate profile is one of the most important source-of-truth domains in the Career Agent.

It will eventually be used by:

Job matching
Resume selection
Resume tailoring
Resume generation
Role profile creation
Career assistant
RAG
Outreach generation
Skill-gap analysis
Application analysis

The profile must contain truthful candidate information supplied or confirmed by the candidate.

The system must never invent candidate facts.

2. Relationship With Phase 10.5

Phase 10.5 already implemented:

Candidate
    │
    └── CandidateProfile

with the basic onboarding fields.

Phase 10.6 must extend the existing domain rather than creating another candidate profile table.

The existing candidate_profiles table remains the canonical basic professional profile.

Phase 10.6 adds related entities:

Candidate
   │
   ├── CandidateProfile
   │
   ├── Experiences
   │      └── ExperienceAchievements
   │
   ├── Education
   │
   └── Projects
          └── ProjectSkills

Skills themselves belong to Phase 10.7.

ProjectSkill may therefore be designed as a relationship that will be completed when the Skills domain is implemented.

3. Goal

After Phase 10.6, an authenticated candidate should be able to maintain a structured professional profile containing:

Basic profile
Name
Email
Phone
Location
Headline
Summary
Years of experience
Current designation
LinkedIn
GitHub
Professional experience
Company
Job title
Employment type
Location
Start date
End date
Current employment status
Description
Achievements
Education
Institution
Degree
Field of study
Start date
End date
Grade/CGPA
Description
Projects
Project name
Description
Role
Start date
End date
Project URL
Repository URL
Project type

The profile should support multiple experiences, education records, and projects.

4. Source-of-Truth Principle

The candidate profile is a verified factual source.

Information can originate from:

Candidate manual input
Candidate-confirmed imported information
Future resume parsing
Future AI-assisted extraction

However, future AI extraction must not automatically become trusted candidate data.

The correct future flow is:

Resume
   ↓
Parser / AI
   ↓
Extracted information
   ↓
Candidate review
   ↓
Candidate confirmation
   ↓
Candidate Profile

For Phase 10.6, implement only the profile management functionality.

Do not implement resume parsing.

5. What Is In Scope
5.1 Existing CandidateProfile

Use the existing candidate_profiles table created in Phase 10.5.

Do not recreate it.

Verify that its existing fields support:

phone
location
headline
summary
years of experience
current designation
LinkedIn
GitHub

If the existing implementation differs from the approved 10.5 design, make the smallest correction necessary.

6. Experience Domain

Create an experiences table.

Suggested fields:

id
candidate_id
company_name
job_title
employment_type
location
start_date
end_date
is_current
description
display_order
created_at
updated_at
Important rules

candidate_id must reference the authenticated candidate.

A candidate may have multiple experiences.

The current experience should have:

is_current = true
end_date = null

Historical experience should normally have:

is_current = false
end_date != null

The backend should validate these relationships.

7. Experience Achievements

Create an experience_achievements table.

Suggested fields:

id
experience_id
achievement
display_order
created_at
updated_at

One experience can have multiple achievements.

Example:

Experience
   ├── Description
   ├── Achievement 1
   ├── Achievement 2
   └── Achievement 3

Achievements should be candidate-provided facts.

The system must not generate fictional achievements.

AI-generated suggestions belong to a later feature and must not automatically be stored as factual achievements.

8. Education Domain

Create an education table.

Suggested fields:

id
candidate_id
institution
degree
field_of_study
start_date
end_date
grade
description
display_order
created_at
updated_at

A candidate may have multiple education records.

Examples:

BCA
Bachelor of Computer Applications
Oxford College
CGPA 7.93

The system must support incomplete education records where appropriate.

For example, a currently pursuing degree may have:

end_date = null
9. Project Domain

Create a projects table.

Suggested fields:

id
candidate_id
name
description
role
project_type
start_date
end_date
project_url
repository_url
display_order
created_at
updated_at

A candidate may have multiple projects.

Projects are important because they provide evidence for future matching and resume generation.

Example:

Candidate
   │
   └── Project
          ├── Name
          ├── Description
          ├── Role
          ├── Repository
          └── Project URL
10. Skills Relationship

Skills are deliberately NOT implemented as a full domain in Phase 10.6.

Skills belong to:

Phase 10.7 — Skills

However, the Phase 10.6 design must not prevent projects and experiences from being associated with skills later.

The future relationship will look like:

Project
   │
   ├── Skill
   ├── Skill
   └── Skill

and:

Candidate
   │
   └── Skills

Do not create the complete Skills system prematurely.

If a foreign-key relationship is required later, design it according to the Phase 3 database architecture.

11. Profile Ownership

Every profile-owned entity must be scoped to the authenticated candidate.

For example:

Candidate A
   └── Experience A1

Candidate B
   └── Experience B1

Candidate A must never be able to access or modify Candidate B's experience.

The browser must not be trusted to provide the candidate identity.

The backend must derive the candidate from:

Firebase ID Token
        ↓
Firebase UID
        ↓
Candidate
        ↓
Candidate-owned records
12. API Design

The APIs should follow the existing versioned API architecture.

Base path:

/api/v1
Candidate profile

Existing:

GET /api/v1/profile

Existing:

POST /api/v1/profile

Add:

PUT /api/v1/profile

or the update method specified by the existing API conventions.

13. Experience APIs

Add:

GET /api/v1/profile/experiences
POST /api/v1/profile/experiences
GET /api/v1/profile/experiences/{experience_id}
PUT /api/v1/profile/experiences/{experience_id}
DELETE /api/v1/profile/experiences/{experience_id}

Achievements:

POST /api/v1/profile/experiences/{experience_id}/achievements
PUT /api/v1/profile/experiences/{experience_id}/achievements/{achievement_id}
DELETE /api/v1/profile/experiences/{experience_id}/achievements/{achievement_id}

Exact endpoint naming should follow the existing Phase 5 API contract conventions.

14. Education APIs

Add:

GET /api/v1/profile/education
POST /api/v1/profile/education
GET /api/v1/profile/education/{education_id}
PUT /api/v1/profile/education/{education_id}
DELETE /api/v1/profile/education/{education_id}
15. Project APIs

Add:

GET /api/v1/profile/projects
POST /api/v1/profile/projects
GET /api/v1/profile/projects/{project_id}
PUT /api/v1/profile/projects/{project_id}
DELETE /api/v1/profile/projects/{project_id}
16. Validation

Use Pydantic schemas.

Validation should include:

Dates

For completed records:

start_date <= end_date

For current employment:

is_current = true
end_date = null
Strings

Apply sensible maximum lengths.

Avoid accepting arbitrarily large text.

URLs

Validate:

LinkedIn URL
GitHub URL
Project URL
Repository URL

using the existing schema conventions.

Ownership

Every resource lookup must verify that it belongs to the authenticated candidate.

17. Backend Architecture

Follow:

API Route
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy
    ↓
PostgreSQL

Do not put business logic directly inside route handlers.

Example:

POST /api/v1/profile/experiences
        ↓
experience route
        ↓
experience service
        ↓
experience repository
        ↓
SQLAlchemy
        ↓
PostgreSQL
18. Repository Layer

Create repositories for the new entities.

For example:

experience_repository.py
education_repository.py
project_repository.py
experience_achievement_repository.py

Repositories should handle database access.

They should not contain HTTP concerns.

19. Service Layer

Create corresponding services.

For example:

experience_service.py
education_service.py
project_service.py

Services should handle:

ownership validation
business rules
creation/update/delete logic
transaction boundaries where appropriate
20. Schemas

Create request/response schemas.

For example:

ExperienceCreate
ExperienceUpdate
ExperienceResponse

ExperienceAchievementCreate
ExperienceAchievementUpdate
ExperienceAchievementResponse

EducationCreate
EducationUpdate
EducationResponse

ProjectCreate
ProjectUpdate
ProjectResponse

Use:

ConfigDict(from_attributes=True)

or the project's established Pydantic convention.

21. Database Relationships

The intended relationships are:

Candidate
   │
   ├── 1 : 1 CandidateProfile
   │
   ├── 1 : N Experience
   │          │
   │          └── 1 : N ExperienceAchievement
   │
   ├── 1 : N Education
   │
   └── 1 : N Project

Foreign keys should use appropriate cascade behavior where approved.

Deleting a candidate should not leave orphaned candidate-owned records.

22. Migration

Create an Alembic migration for the new tables.

The migration should create:

experiences
experience_achievements
education
projects

Do not modify existing migrations unnecessarily.

Migration process:

SQLAlchemy models
        ↓
Alembic revision
        ↓
Inspect migration
        ↓
alembic upgrade head
        ↓
Verify PostgreSQL schema
23. Candidate Profile Completeness

Phase 10.6 should introduce the concept of profile completeness, but it should remain deterministic.

Do not use an LLM to calculate basic completeness.

Example:

Basic profile          ✓
Experience             ✓
Education              ✓
Projects               ✓
Skills                 pending Phase 10.7

A simple service may calculate:

profile completeness = completed required sections / required sections

However, the exact scoring formula should remain simple and explainable.

Do not create an authoritative "candidate quality score".

This is completeness, not candidate ranking.

24. Frontend Scope

Phase 10.6 should also create the basic Angular profile-management UI required to use the new backend functionality.

The UI should allow the authenticated candidate to:

View profile
Edit basic profile
Add experience
Edit experience
Delete experience
Add achievements
Add education
Edit education
Delete education
Add projects
Edit projects
Delete projects

The UI should be built using the approved Angular architecture.

Use:

Angular standalone components
Angular Material
Tailwind CSS
Typed API services

Do not build the complete career dashboard yet.

Do not build resume generation UI.

Do not build job discovery UI.

Do not build skills management UI.

Those belong to later phases.

25. Frontend Architecture

Follow:

Component
   ↓
Angular Service
   ↓
HTTP API
   ↓
FastAPI

Do not place API calls directly throughout components.

Use reusable typed services.

For example:

profile.service.ts
experience.service.ts
education.service.ts
project.service.ts

The exact organization should follow the existing Angular project structure.

26. Error Handling

The frontend should handle:

401 Unauthorized
403 Forbidden
404 Not Found
422 Validation Error
500 Server Error

Do not expose internal backend errors directly to the user.

Display understandable validation messages.

27. Security

The following must be enforced:

Firebase authentication
Backend authorization
Candidate ownership
Input validation
URL validation
No candidate ID trust from browser
No sensitive information in logs
No secrets in frontend source
No direct database access from Angular
28. Testing
Backend unit tests

Test:

Profile update
Experience creation
Experience update
Experience deletion
Education creation
Education update
Education deletion
Project creation
Project update
Project deletion
Achievement management
Validation rules
Authorization tests

At minimum:

Candidate A cannot read Candidate B's experience
Candidate A cannot update Candidate B's experience
Candidate A cannot delete Candidate B's project
Database tests

Verify:

Foreign keys
Unique constraints where applicable
Cascade behavior
Migration success
API tests

Verify:

401 without authentication
404 for non-owned resources where appropriate
422 invalid data
Successful CRUD operations
Frontend tests

Test important profile interactions and API service behavior.

29. Manual Verification

After implementation:

Profile
Login
 ↓
Open Profile
 ↓
Edit basic profile
 ↓
Save
 ↓
Refresh
 ↓
Data remains
Experience
Add experience
 ↓
Save
 ↓
Refresh
 ↓
Experience remains
Ownership
Candidate A
 ↓
cannot access Candidate B's experience
Education
Add education
 ↓
Save
 ↓
Refresh
 ↓
Data remains
Projects
Add project
 ↓
Save
 ↓
Refresh
 ↓
Data remains
30. Important Non-Goals

Do NOT implement:

Skills management
Skill normalization
Skill aliases
Resume upload
Resume parsing
Role profiles
Preferences
Company discovery
Job discovery
JD analysis
Matching
Resume tailoring
Applications
RAG
Agents
Career assistant

Those belong to later phases.

31. Definition of Done

Phase 10.6 is complete when:

Backend
CandidateProfile can be updated
Experience CRUD works
Experience achievements work
Education CRUD works
Project CRUD works
Ownership is enforced
Validation works
Alembic migration works
PostgreSQL schema is verified
Frontend
Candidate can view profile
Candidate can edit profile
Candidate can manage experience
Candidate can manage education
Candidate can manage projects
Important errors are handled
Security
Authentication enforced
Candidate ownership enforced
No browser-provided candidate ID trusted
Testing
Unit tests pass
API tests pass
Authorization tests pass
Database tests pass
Angular build passes
Verification

A candidate can maintain a complete factual professional profile through the application.

32. Expected Data Flow

The complete flow should be:

Angular Profile UI
        ↓
Firebase authenticated request
        ↓
FastAPI
        ↓
Verify Firebase ID token
        ↓
Resolve Firebase UID
        ↓
Resolve Candidate
        ↓
Profile Service
        ↓
Repository
        ↓
SQLAlchemy
        ↓
PostgreSQL
        ↓
Response
        ↓
Angular UI
33. Future Usage

The profile created here becomes input for later features.

For example:

Candidate Profile
       │
       ├──────────────→ Role Profile
       │
       ├──────────────→ Resume Selection
       │
       ├──────────────→ Resume Tailoring
       │
       ├──────────────→ Candidate Matching
       │
       ├──────────────→ RAG
       │
       └──────────────→ Career Assistant

The profile therefore acts as an important factual foundation for the Career Agent.

34. Engineering Principles

The implementation must follow these principles:

Candidate data is source-of-truth data.
AI must not invent candidate facts.
PostgreSQL remains the source of truth.
Candidate ownership is enforced by the backend.
Firebase UID is used for external identity.
Candidate UUID is used for internal identity.
API routes remain thin.
Business logic belongs in services.
Database access belongs in repositories.
Schema changes use Alembic.
Phase boundaries must be respected.
Do not implement future features prematurely.
35. Deliverables

Phase 10.6 should produce:

Backend
├── CandidateProfile update functionality
├── Experience domain
├── ExperienceAchievement domain
├── Education domain
├── Project domain
├── Repositories
├── Services
├── Schemas
├── API routes
├── Alembic migration
└── Tests

Frontend
├── Profile page/section
├── Experience management
├── Education management
├── Project management
├── Typed API services
└── Tests
36. Phase Completion Report

At completion, report:

Implementation
What was implemented
Files created
Files modified
Database
Tables
Relationships
Migration
Migration status
API
Endpoints
Request schemas
Response schemas
Frontend
Components
Services
Routes
Security
Authentication
Authorization
Ownership verification
Testing
Unit tests
Integration tests
API tests
Authorization tests
Angular tests
Build results
Verification
Manual verification
PostgreSQL verification
Problems
Errors
Warnings
Unresolved issues
Architecture
Deviations from approved architecture
Decisions made