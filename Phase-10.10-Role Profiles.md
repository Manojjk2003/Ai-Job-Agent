Phase 10.10 — Role Profiles
# Phase 10.10 — Role Profiles

## 1. Purpose

Phase 10.10 introduces **Role Profiles**.

A candidate should not be represented by one generic job profile.

The same candidate may realistically apply for:

- Frontend Engineer
- Full Stack Engineer
- Forward Deployed Engineer
- Junior Software Engineer
- Backend Engineer

Each role can emphasize different parts of the candidate's real experience.

Therefore, the system needs a role-specific layer between the candidate's master profile and a particular job.

The architecture becomes:

Candidate
    ↓
Master Candidate Profile
    ↓
Role Profiles
    ├── Frontend Engineer
    ├── Full Stack Engineer
    ├── Forward Deployed Engineer
    └── Junior Software Engineer
          ↓
Job
          ↓
Matching

A Role Profile does NOT create new experience.

It selects and organizes verified candidate information for a particular target role.

---

# 2. Core Principle

The master candidate profile is the source of truth.

Role profiles are derived views/configurations of that source of truth.

Example:

Master profile:

Skills:
- Angular
- TypeScript
- React
- Python
- FastAPI
- MySQL
- Firebase
- AWS
- Docker

Experience:
- Software Engineer
- Internship experience
- Projects

The candidate may create:

Frontend Engineer profile:

Skills emphasized:
- Angular
- TypeScript
- React
- HTML
- CSS

Full Stack Engineer profile:

Skills emphasized:
- Angular
- TypeScript
- Python
- FastAPI
- MySQL
- AWS
- Docker

Forward Deployed Engineer profile:

Skills emphasized:
- Full-stack development
- Requirements gathering
- HLD
- LLD
- Data modeling
- Debugging
- Client/product interaction

The role profile cannot claim:

```text
Kubernetes

unless Kubernetes exists in the verified candidate data.

3. Why Role Profiles Are Necessary

Using one resume/profile for every job creates several problems.

Example:

A Frontend Engineer JD may emphasize:

Angular
TypeScript
HTML
CSS
REST APIs

A Forward Deployed Engineer JD may emphasize:

Customer requirements
Solution design
Deployment
Debugging
Communication
Full-stack development

The candidate may have evidence for both.

A single generic profile cannot emphasize both appropriately.

Therefore:

Master Profile
       ↓
Role Profile
       ↓
Job-specific Resume

This becomes one of the core foundations of the product.

4. Scope

Phase 10.10 includes:

Role profile database model
Role profile CRUD
Role-specific target designation
Role summary
Role-specific skill selection
Role-specific experience selection
Role-specific project selection
Role-specific education selection where needed
Role profile ordering/prioritization
Default role profile
Role profile activation/archive
Candidate ownership
Backend APIs
Frontend role-profile management
Validation
Tests
5. Explicitly NOT Included

Do NOT implement:

Job matching
JD analysis
Resume tailoring
Resume generation
ATS scoring
AI job recommendations
Company discovery
Job discovery
RAG
Qdrant indexing
Agent workflows
Automatic applications
Automatic profile creation from an uploaded resume
Automatic invention of skills
Automatic Gemini-generated claims

AI may be introduced later where appropriate, but it must not replace the source-of-truth model.

6. Relationship With Previous Phases

The existing architecture is:

10.5 Candidate Onboarding
↓
10.6 Candidate Profile
↓
10.7 Skills
↓
10.8 Resume Upload
↓
10.9 Resume Parsing
↓
10.10 Role Profiles

Role Profiles use information established by these previous domains.

They do not duplicate them.

7. Master Profile vs Role Profile

This distinction must be maintained.

Master Candidate Profile

Answers:

Who is this candidate?

Contains the candidate's real:

Experience
Skills
Projects
Education
Achievements
Contact information
Links
Other verified career information
Role Profile

Answers:

How should this candidate position themselves for a particular type of role?

It can define:

Target role
Role-specific headline
Role-specific summary
Preferred skills to emphasize
Relevant experiences
Relevant projects
Priority/order
Target seniority
Target locations/preferences where appropriate

It must not create fictional experience.

8. Example

Suppose the master profile contains:

Skills:
Angular
TypeScript
React
Python
FastAPI
MySQL
AWS
Docker

Experience:
Software Engineer

Projects:
Teacher Progress Tracking
Learning Platform
Website

The candidate creates:

Role Profile:
Frontend Engineer

It may select:

Skills:
Angular
TypeScript
React

Projects:
Learning Platform
Teacher Progress Tracking

Then another:

Role Profile:
Full Stack Engineer

may select:

Skills:
Angular
TypeScript
Python
FastAPI
MySQL
AWS
Docker

Projects:
Teacher Progress Tracking
Learning Platform

Both are valid because they select existing information.

9. Database Model

The database already contains the candidate and related profile domains.

Add:

role_profiles

Recommended relationships:

Candidate
   |
   +---- RoleProfile
            |
            +---- RoleProfileSkill
            |
            +---- RoleProfileExperience
            |
            +---- RoleProfileProject

Do not duplicate the underlying skill, experience, or project records.

Use relationship tables.

10. role_profiles Table

Recommended fields:

role_profiles
--------------------------------
id
candidate_id
name
target_designation
headline
summary
target_seniority
is_default
is_active
created_at
updated_at
id

UUID primary key.

candidate_id

Foreign key to:

candidates.id

Every role profile belongs to exactly one candidate.

name

User-friendly profile name.

Example:

Frontend Engineer
Full Stack Engineer
Forward Deployed Engineer

This does not have to be identical to the job title.

target_designation

The primary target designation.

Example:

Frontend Engineer
headline

Optional role-specific professional headline.

Example:

Frontend Engineer focused on Angular, TypeScript and modern web applications
summary

Optional role-specific summary.

This is controlled candidate content.

Do not automatically invent it.

target_seniority

Optional controlled value such as:

intern
junior
mid
senior
lead

or another approved enum strategy.

Do not assume the candidate's seniority based only on an LLM.

is_default

Whether this is the candidate's default role profile.

A candidate should normally have at most one default profile.

is_active

Allows a profile to be archived without deleting historical references.

timestamps

Standard:

created_at
updated_at
11. Role Profile Skill Relationship

Create:

role_profile_skills

Recommended fields:

id
role_profile_id
candidate_skill_id
priority
is_primary
created_at

The important relationship is:

RoleProfile
      ↓
CandidateSkill
      ↓
Skill

Do NOT create a separate copy of the skill.

For example:

role_profile_skills

should reference:

candidate_skills.id

not:

skills.name

This ensures the role profile can only select skills already associated with the candidate.

12. Skill Priority

A role profile should be able to prioritize skills.

Example:

Frontend Engineer

1. Angular
2. TypeScript
3. React
4. REST API
5. HTML
6. CSS

Recommended field:

priority

Lower number can represent higher priority.

Example:

Angular       1
TypeScript    2
React         3
REST API      4

The exact ordering convention must remain consistent throughout the application.

13. is_primary

A role profile may mark some skills as primary.

Example:

Angular      primary
TypeScript   primary
React        primary
AWS          secondary

This becomes useful later when tailoring resumes.

14. Role Profile Experience

Create:

role_profile_experiences

Recommended fields:

id
role_profile_id
experience_id
priority
is_primary
created_at

The experience_id must reference an existing candidate experience.

Example:

Candidate Experience
        ↓
Software Engineer
        ↓
Role Profile
        ↓
Frontend Engineer

The role profile selects it.

It does not duplicate the experience.

15. Role Profile Projects

Create:

role_profile_projects

Recommended fields:

id
role_profile_id
project_id
priority
is_primary
created_at

Again, this is a relationship.

The role profile cannot create a project that does not exist in the candidate's master profile.

16. Education

For MVP, education does not necessarily need a relationship table.

Education is usually part of the candidate's overall profile and can remain globally available.

However, if the existing approved database design contains multiple education records and later requirements require role-specific selection, add:

role_profile_education

Do not duplicate education records.

Only introduce this relationship if it is actually required by the existing Phase 10.6 design.

17. Candidate Ownership

Every role profile belongs to:

candidate_id

The backend must determine candidate ownership from the verified Firebase token.

Never trust a browser-supplied candidate ID.

Flow:

Firebase Token
      ↓
Verify Token
      ↓
Firebase UID
      ↓
Candidate
      ↓
Role Profile
18. Default Role Profile

A candidate may have multiple role profiles.

Example:

Frontend Engineer       default
Full Stack Engineer     active
FDE                     active
Backend Engineer        archived

Only one role profile should be the default.

When a candidate sets another profile as default:

Old Default
    ↓
is_default = false

New Default
    ↓
is_default = true

This should happen atomically.

19. Active vs Archived

Use:

is_active

instead of immediately deleting role profiles.

Example:

Frontend Engineer
Full Stack Engineer
FDE

If the candidate stops targeting FDE:

FDE
is_active = false

Historical applications/resumes may still refer to it.

This is important for application history.

20. Role Profile Name vs Target Designation

Keep these concepts separate.

Example:

name:
"Startup Full Stack"

target_designation:
"Full Stack Engineer"

Another:

name:
"FDE - Product/Customer"

target_designation:
"Forward Deployed Engineer"

The name is for the candidate's organization.

The designation is the actual target role.

21. Role Profile Summary

A role profile may contain a tailored summary.

Example:

Full Stack Engineer with experience building Angular and FastAPI applications,
working with relational databases, cloud infrastructure and REST APIs.

This summary must be based on verified candidate information.

Do not automatically claim:

5 years of experience

if the candidate does not have it.

22. Role Profile Skill Validation

When adding a skill:

POST /role-profile/skills

the backend must verify:

candidate_skill belongs to authenticated candidate

This prevents:

Candidate A
   ↓
Role Profile A
   ↓
Candidate B's Skill

which must never be possible.

23. Role Profile Experience Validation

Same rule:

role_profile_experiences.experience_id

must belong to the authenticated candidate.

24. Role Profile Project Validation

Same rule:

role_profile_projects.project_id

must belong to the authenticated candidate.

25. APIs

Recommended endpoints:

GET    /api/v1/role-profiles
POST   /api/v1/role-profiles
GET    /api/v1/role-profiles/{role_profile_id}
PUT    /api/v1/role-profiles/{role_profile_id}
DELETE /api/v1/role-profiles/{role_profile_id}

For default:

POST /api/v1/role-profiles/{role_profile_id}/set-default

For skills:

GET    /api/v1/role-profiles/{role_profile_id}/skills
POST   /api/v1/role-profiles/{role_profile_id}/skills
DELETE /api/v1/role-profiles/{role_profile_id}/skills/{candidate_skill_id}

For experiences:

GET    /api/v1/role-profiles/{role_profile_id}/experiences
POST   /api/v1/role-profiles/{role_profile_id}/experiences
DELETE /api/v1/role-profiles/{role_profile_id}/experiences/{experience_id}

For projects:

GET    /api/v1/role-profiles/{role_profile_id}/projects
POST   /api/v1/role-profiles/{role_profile_id}/projects
DELETE /api/v1/role-profiles/{role_profile_id}/projects/{project_id}

For archive:

POST /api/v1/role-profiles/{role_profile_id}/archive

Alternatively, archive can be handled through the main update endpoint if that matches the existing API convention.

Do not create redundant APIs if the existing project conventions already provide an appropriate pattern.

26. Create Role Profile

Example request:

{
  "name": "Frontend Engineer",
  "target_designation": "Frontend Engineer",
  "headline": "Frontend Engineer focused on Angular and TypeScript",
  "summary": "Frontend-focused software engineer experienced in building web applications.",
  "target_seniority": "junior"
}

The backend automatically determines:

candidate_id

from authentication.

It must NOT come from the request body.

27. Update Role Profile

The candidate can update:

name
target designation
headline
summary
target seniority
active state

Do not allow changing:

candidate_id
28. Add Skill

Example:

{
  "candidate_skill_id": "uuid",
  "priority": 1,
  "is_primary": true
}

The backend verifies the skill belongs to the candidate.

29. Add Experience

Example:

{
  "experience_id": "uuid",
  "priority": 1,
  "is_primary": true
}

The backend verifies ownership.

30. Add Project

Example:

{
  "project_id": "uuid",
  "priority": 1,
  "is_primary": true
}

Again, verify candidate ownership.

31. Duplicate Relationship Prevention

A role profile must not contain the same skill twice.

For example:

Frontend Engineer
   ↓
Angular
Angular
Angular

must be rejected.

Use database-level unique constraints such as:

(role_profile_id, candidate_skill_id)

Likewise:

(role_profile_id, experience_id)
(role_profile_id, project_id)
32. Ordering

The candidate should be able to control ordering.

Example:

Skills

1. Angular
2. TypeScript
3. React
4. FastAPI

Later, the resume generator can use this ordering.

Do not hard-code ordering in the frontend.

33. Frontend

Add a Role Profiles section.

Example:

My Role Profiles

┌───────────────────────────────┐
│ Frontend Engineer             │
│ Default                       │
│ Angular · TypeScript · React  │
│                               │
│ [Open] [Edit]                 │
└───────────────────────────────┘

┌───────────────────────────────┐
│ Full Stack Engineer           │
│ Angular · FastAPI · MySQL     │
│                               │
│ [Open] [Edit]                 │
└───────────────────────────────┘
34. Create Role Profile UI

Provide:

Role Profile Name
Target Designation
Headline
Summary
Target Seniority

Then allow selection of:

Skills
Experiences
Projects

Only information already belonging to the candidate should be selectable.

35. Role Profile Detail Page

Example:

Frontend Engineer

Target:
Frontend Engineer

Headline:
Frontend Engineer focused on Angular and TypeScript

Summary:
...

Primary Skills:
1. Angular
2. TypeScript
3. React

Relevant Experience:
1. Software Engineer

Relevant Projects:
1. Teacher Progress Tracking
2. Learning Platform
36. Candidate-Friendly Explanation

The UI should explain:

This profile does not create new experience.
It controls which of your existing skills, experience and projects
are emphasized for this type of role.

This makes the architecture understandable to the user.

37. No Automatic Role Profiles

Do not automatically create:

Frontend Engineer
Backend Engineer
Full Stack Engineer
FDE

just because the candidate has certain skills.

The candidate can manually create profiles during this phase.

AI-assisted role-profile suggestions may be introduced later.

38. AI Boundary

If AI is introduced later, the safe architecture is:

Master Profile
      ↓
AI Suggestion
      ↓
Candidate Review
      ↓
Role Profile

Not:

Master Profile
      ↓
AI
      ↓
Automatically modify candidate data

Candidate approval remains important.

39. Resume Relationship

A role profile is NOT itself a resume.

Relationship:

Candidate
   ↓
Role Profile
   ↓
Selected verified facts
   ↓
Resume Selection
   ↓
Tailored Resume

The resume selection/tailoring work belongs to later phases.

40. Existing Resume Parsing Relationship

Phase 10.9 produced:

Parsed Resume

That data can later help the candidate build or verify their profile.

However:

Parsed Resume

must not automatically become:

Role Profile

The candidate must control the confirmed profile.

41. Database Constraints

Recommended:

role_profiles.candidate_id
    → candidates.id

role_profile_skills.role_profile_id
    → role_profiles.id

role_profile_skills.candidate_skill_id
    → candidate_skills.id

role_profile_experiences.role_profile_id
    → role_profiles.id

role_profile_experiences.experience_id
    → experiences.id

role_profile_projects.role_profile_id
    → role_profiles.id

role_profile_projects.project_id
    → projects.id

Add unique constraints on relationship pairs.

42. Default Profile Constraint

The database/application must enforce one default profile per candidate.

If PostgreSQL partial indexes are used, a conceptual constraint is:

UNIQUE(candidate_id)
WHERE is_default = true

If the existing migration strategy does not support this directly, enforce it transactionally in the service layer plus an appropriate database strategy.

Do not rely only on frontend logic.

43. Delete Behavior

Do not casually hard-delete a role profile that may be referenced by:

resumes
applications
application history

For MVP, archive is preferred.

If the API exposes DELETE, it should either:

archive the profile, or
reject deletion when historical dependencies exist.

Do not destroy historical application context.

44. Service Layer

Create:

backend/app/services/role_profile_service.py

Responsibilities:

Create profile
Get profiles
Update profile
Archive profile
Set default
Add/remove skills
Add/remove experiences
Add/remove projects
Validate candidate ownership
Validate relationship ownership
Maintain ordering
Enforce default-profile behavior

The service should not contain raw HTTP logic.

45. Repository Layer

Create:

backend/app/repositories/role_profile_repository.py

Potentially separate repositories for relationship operations if that matches the existing project architecture.

Responsibilities:

Database queries
CRUD
Relationship persistence
Ordering
Default-profile lookup

Do not put Firebase verification inside repositories.

46. Schemas

Add Pydantic schemas such as:

RoleProfileCreate
RoleProfileUpdate
RoleProfileResponse

RoleProfileSkillCreate
RoleProfileSkillResponse

RoleProfileExperienceCreate
RoleProfileExperienceResponse

RoleProfileProjectCreate
RoleProfileProjectResponse

Keep request and response models separate where useful.

47. API Response

A complete role-profile response may look like:

{
  "id": "uuid",
  "name": "Frontend Engineer",
  "target_designation": "Frontend Engineer",
  "headline": "Frontend Engineer focused on Angular and TypeScript",
  "summary": "...",
  "target_seniority": "junior",
  "is_default": true,
  "is_active": true,
  "skills": [
    {
      "candidate_skill_id": "uuid",
      "skill_name": "Angular",
      "priority": 1,
      "is_primary": true
    }
  ],
  "experiences": [],
  "projects": []
}

The response should provide enough information for the UI without exposing internal database details unnecessarily.

48. Validation

Validate:

Name

Cannot be empty.

Target designation

Cannot be empty.

Summary/headline

Apply reasonable maximum lengths.

Seniority

Only accepted controlled values.

Skill

Must belong to candidate.

Experience

Must belong to candidate.

Project

Must belong to candidate.

Priority

Must be positive.

49. Security Tests

Test that:

Candidate A
   ↓
cannot access Candidate B's role profile

Also test:

Candidate A
   ↓
Role Profile A
   ↓
cannot attach Candidate B's skill

and:

Candidate A
   ↓
Role Profile A
   ↓
cannot attach Candidate B's experience

and:

Candidate A
   ↓
Role Profile A
   ↓
cannot attach Candidate B's project

These tests are essential.

50. Backend Tests

At minimum:

Create role profile
List role profiles
Get role profile
Update role profile
Archive role profile
Set default role profile
Add skill
Remove skill
Add experience
Remove experience
Add project
Remove project
Duplicate relationship rejection
Invalid candidate relationship rejection
Ownership rejection
Authentication rejection
51. Default Profile Tests

Test:

Create profile A as default
Create profile B as default

Expected:

A.is_default = false
B.is_default = true

Also test:

Set existing profile as default

and verify there is never more than one default profile.

52. Frontend Tests

Test:

Role profile list
Create profile
Edit profile
View profile
Set default
Archive
Add skill
Remove skill
Add project
Remove project
Add experience
Remove experience

The Angular production build must pass.

53. Migration Validation

After creating the migration:

alembic upgrade head

must succeed.

Verify:

role_profiles
role_profile_skills
role_profile_experiences
role_profile_projects

exist correctly.

Also verify the existing migrations still work from an empty database.

54. Existing Functionality

Phase 10.10 must not break:

Authentication
Candidate onboarding
Candidate profile
Skills
Resume upload
Resume parsing

Run the existing test suite after implementation.

55. Important Architecture Rule

Do not create this:

role_profiles
    skills TEXT
    experiences TEXT
    projects TEXT

This would duplicate the source-of-truth data.

Prefer:

role_profiles
       |
       +---- role_profile_skills ----> candidate_skills
       |
       +---- role_profile_experiences -> experiences
       |
       +---- role_profile_projects ----> projects

This allows the candidate to update their master data once.

56. Why This Matters Later

Suppose the candidate updates:

Angular

from:

Intermediate

to:

Advanced

The role profiles that reference Angular should automatically see the updated canonical skill information.

If the role profile had copied:

Angular
Intermediate

the system could become inconsistent.

That is why role profiles reference canonical records.

57. Future Job Matching

Later:

Job
 ↓
JD requirements
 ↓
Matching Engine
 ↓
Candidate Master Profile
 +
Role Profile
 +
Evidence
 ↓
Match Result

The role profile can tell the system:

This is the way I want to position myself for this category of role.

It does NOT change the underlying facts.

58. Future Resume Tailoring

Later:

Job Description
        ↓
Matching
        ↓
Role Profile
        ↓
Relevant Experience
        ↓
Relevant Projects
        ↓
Relevant Skills
        ↓
Base Resume
        ↓
Tailored Resume

This is why Role Profiles need ordering and prioritization now.

59. Future AI Suggestions

Later the system can say:

Based on your profile, you may want to create:

Frontend Engineer
Full Stack Engineer
Forward Deployed Engineer

But the system should ask for confirmation.

Example:

Suggested Role Profile

Forward Deployed Engineer

Why:
Your profile contains evidence of requirements gathering,
solution design, full-stack development and deployment.

[Create Profile]
[Ignore]

That belongs later.

60. Acceptance Criteria

Phase 10.10 is complete only when:

 Role profiles can be created.
 Role profiles can be listed.
 Role profiles can be viewed.
 Role profiles can be updated.
 Role profiles can be archived.
 One default role profile can be maintained.
 Skills can be associated.
 Experiences can be associated.
 Projects can be associated.
 Ordering/priority works.
 Primary flags work.
 Duplicate relationships are prevented.
 Candidate ownership is enforced.
 Cross-candidate relationships are rejected.
 Master profile data is not duplicated.
 No fictional skills/experience can be added.
 No automatic AI profile generation is introduced.
 Existing authentication continues working.
 Existing candidate profile continues working.
 Existing skills continue working.
 Existing resume upload continues working.
 Existing resume parsing continues working.
 Backend tests pass.
 Frontend tests/build pass.
 Alembic migration passes.
61. Implementation Order

Implement sequentially:

Inspect Phase 10.6 implementation.
Inspect existing skills, experiences and projects models.
Inspect Phase 10.9 implementation.
Add role profile models.
Add relationship models.
Create Alembic migration.
Add repositories.
Add Pydantic schemas.
Add service layer.
Add API endpoints.
Implement default-profile handling.
Implement ownership validation.
Implement relationship validation.
Implement frontend role-profile service.
Implement role-profile UI.
Add backend tests.
Add frontend tests.
Run migrations.
Run full test suite.
Run Angular build.
Inspect implementation.
Fix issues.
Verify no architecture deviation.
62. Codex Instructions

Before implementation:

Read this entire document.
Inspect the current repository.
Inspect the actual Phase 10.6 implementation.
Inspect the actual Phase 10.7 implementation.
Inspect the actual Phase 10.9 implementation.
Reuse existing architecture and naming conventions.
Do not assume the example filenames in this document exactly match the repository.
Do not recreate existing tables.
Do not duplicate candidate data.
Do not redesign previous phases.

Implement ONLY Phase 10.10.

Do NOT implement:

10.11 Preferences
Company Discovery
Hiring Source Discovery
Job Discovery
JD Analysis
Matching
Resume Selection
Resume Tailoring
Applications
RAG
Agents
Career Assistant

If an existing implementation differs from this document in a way that requires an architectural change, stop and report the contradiction before making a major change.

63. Final Implementation Report

After implementation provide:

Implemented

Exact functionality implemented.

Database

List:

tables
columns
relationships
constraints
indexes
migrations
APIs

List every endpoint.

Frontend

Explain:

pages/components
create flow
edit flow
skill selection
experience selection
project selection
default profile
archive
Security

Explain:

Firebase authentication
candidate ownership
relationship ownership
Tests

Provide actual results:

Backend tests: X passed
Frontend tests: X passed
Angular build: PASS/FAIL
Alembic migration: PASS/FAIL
Integration tests: X passed
Warnings

List warnings separately.

Errors

List unresolved errors separately.

Deviations

For every deviation:

Expected:
...

Implemented:
...

Reason:
...
Remaining

Confirm that Phase 10.11 and later were NOT implemented.


### The key idea for 10.10

This is a **very important piece of the product architecture**.

We are deliberately creating:

**Master candidate truth → Role-specific positioning → Job-specific tailoring**

rather than:

**One resume → send everywhere**

For your own use, you could eventually have:

```text
My Master Profile
│
├── Frontend Engineer
│
├── Full Stack Engineer
│
├── Forward Deployed Engineer
│
└── Junior Software Engineer