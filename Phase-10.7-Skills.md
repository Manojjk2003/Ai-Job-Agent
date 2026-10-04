Phase 10.7 — Skills
1. Purpose

Phase 10.7 introduces the Skills domain into the Career Agent.

The system needs to understand skills as structured entities rather than storing them as arbitrary comma-separated text.

For example, these should not be treated as completely unrelated strings:

JavaScript
JS
Javascript
ECMAScript

They may represent the same or closely related skill.

The Skills domain will eventually support:

Candidate skill management
Skill normalization
Skill aliases
Skill categories
Skill evidence
Job skill requirements
Candidate/job matching
Resume tailoring
Skill-gap analysis
RAG
Career Assistant
Skill demand intelligence

Phase 10.7 establishes the foundation for these capabilities.

2. Scope

Phase 10.7 includes:

Skill
SkillAlias
CandidateSkill
SkillEvidence

and the APIs/UI necessary for candidates to manage their skills.

It should also provide the foundation for associating skills with candidate experiences/projects later.

3. Relationship With Previous Phases

The current domain becomes:

Candidate
   │
   ├── CandidateProfile
   │
   ├── Experiences
   │
   ├── Education
   │
   ├── Projects
   │
   └── CandidateSkills
             │
             ▼
           Skill
             │
             └── SkillAlias

Candidate skills are therefore not stored as plain strings inside CandidateProfile.

Instead:

Candidate
   │
   └── CandidateSkill
           │
           ▼
         Skill

This allows the same canonical skill to be reused across candidates, jobs, projects, and experiences.

4. Core Principle

A skill must have a canonical identity.

For example:

Canonical Skill:
JavaScript

Aliases:
JS
Javascript
ECMAScript

The database should store:

skill.id = UUID
skill.name = "JavaScript"

rather than creating separate canonical skills for every spelling variation.

5. Skill Entity

Create a skills table.

Suggested fields:

id
name
normalized_name
description
category
is_active
created_at
updated_at
Example
id: UUID
name: JavaScript
normalized_name: javascript
category: Programming Language
is_active: true
6. Skill Normalization

normalized_name should be used for consistent lookup.

For example:

JavaScript → javascript
JAVASCRIPT → javascript
Javascript → javascript

The normalization process should be deterministic.

Do not use an LLM for basic normalization.

A simple normalization process may include:

trimming whitespace
lowercase conversion
collapsing repeated whitespace

More advanced normalization can be added later.

7. Skill Alias

Create a skill_aliases table.

Suggested fields:

id
skill_id
alias
normalized_alias
created_at

Relationship:

Skill
  │
  ├── Alias
  ├── Alias
  └── Alias

Example:

Skill:
JavaScript

Aliases:
JS
Javascript
ECMAScript
8. CandidateSkill

Create a candidate_skills table.

Suggested fields:

id
candidate_id
skill_id
proficiency
years_experience
is_primary
created_at
updated_at

This represents:

Candidate X has Skill Y.

Example:

Candidate:
Manoj

CandidateSkill:
JavaScript
proficiency: intermediate
years_experience: 2

The system should not require the candidate to provide every field.

For example:

skill = Python
proficiency = null
years_experience = null

can still be valid.

9. Proficiency

For MVP, proficiency should use a controlled set of values.

Example:

beginner
intermediate
advanced
expert

Do not create an arbitrary numeric score.

The exact allowed values should be represented as a backend enum or controlled validation set.

Later we may introduce more sophisticated skill assessment.

10. Skill Evidence

Create a skill_evidence table.

Suggested fields:

id
candidate_skill_id
evidence_type
reference_id
description
created_at

Possible evidence types:

experience
project
education
certification
candidate_claim

Example:

CandidateSkill:
FastAPI

Evidence:
Type: project
Reference: Project UUID
Description:
"Used FastAPI to build REST APIs."

This is extremely important for future matching.

The system should eventually be able to answer:

"Why do you think this candidate has FastAPI experience?"

Instead of simply saying:

"The candidate has FastAPI."

11. Evidence Principle

A candidate skill should ideally be connected to evidence.

However, Phase 10.7 should allow a candidate to explicitly claim a skill without evidence.

For example:

CandidateSkill
    │
    ├── Candidate claim
    │
    ├── Project evidence
    │
    └── Experience evidence

The system must distinguish between:

Candidate-provided claim

and:

Evidence-backed skill

Do not treat every skill as equally strong evidence.

12. Skill Categories

Skills should support categories.

Initial categories may include:

Programming Language
Frontend
Backend
Database
Cloud
DevOps
Framework
Library
Testing
Tools
AI / ML
Data
Security
Architecture
Soft Skill
Other

Do not over-engineer the taxonomy.

The category system should be extensible.

13. Candidate Skill APIs

Base API:

/api/v1/profile/skills
List skills
GET /api/v1/profile/skills
Add skill
POST /api/v1/profile/skills
Get individual candidate skill
GET /api/v1/profile/skills/{candidate_skill_id}
Update candidate skill
PUT /api/v1/profile/skills/{candidate_skill_id}
Remove skill
DELETE /api/v1/profile/skills/{candidate_skill_id}
14. Skill Search

The candidate should not have to type an arbitrary skill every time.

Provide:

GET /api/v1/skills

with optional search:

GET /api/v1/skills?search=java

The API should return canonical skills.

Example:

[
  {
    "id": "...",
    "name": "Java",
    "category": "Programming Language"
  },
  {
    "id": "...",
    "name": "JavaScript",
    "category": "Programming Language"
  }
]
15. Skill Alias Search

When searching for:

JS

the system should be capable of finding:

JavaScript

using the alias relationship.

This is a foundation for future job matching.

16. Duplicate Prevention

A candidate should not be able to add the same canonical skill twice.

For example:

Candidate
 ├── JavaScript
 └── JavaScript

must not be allowed.

A suitable unique constraint should exist around:

candidate_id + skill_id
17. Candidate Ownership

All candidate skill operations must follow:

Firebase ID Token
       ↓
Firebase UID
       ↓
Candidate
       ↓
CandidateSkill

Never trust:

candidate_id

provided by the frontend.

Candidate A must not be able to manipulate Candidate B's skills.

18. Skill Creation Policy

For the MVP, candidate users should preferably select from existing canonical skills.

The application should not blindly create a new canonical skill every time a user enters text.

For example:

User enters:
"JS"

System:
Search canonical skills
      ↓
Find JavaScript
      ↓
Offer JavaScript

If a skill does not exist, the system may support a controlled creation workflow.

However, uncontrolled user-generated canonical skills should be avoided.

A future Skill Intelligence system can handle better normalization.

19. Repository Architecture

Follow the existing pattern:

API
 ↓
Service
 ↓
Repository
 ↓
SQLAlchemy
 ↓
PostgreSQL

Suggested repositories:

skill_repository.py
candidate_skill_repository.py
skill_alias_repository.py
skill_evidence_repository.py
20. Service Layer

Suggested services:

skill_service.py
candidate_skill_service.py
skill_evidence_service.py

Services should handle:

Skill lookup
Normalization
Candidate ownership
Duplicate prevention
Candidate skill creation
Candidate skill updates
Candidate skill deletion
Evidence management
21. Pydantic Schemas

Create schemas such as:

SkillResponse

SkillAliasResponse

CandidateSkillCreate

CandidateSkillUpdate

CandidateSkillResponse

SkillEvidenceCreate

SkillEvidenceResponse

Validation should be explicit.

For example:

proficiency:
beginner | intermediate | advanced | expert
22. Database Relationships

The intended relationships:

Candidate
   │
   └── 1:N CandidateSkill
                 │
                 └── N:1 Skill
                         │
                         └── 1:N SkillAlias

CandidateSkill
   │
   └── 1:N SkillEvidence
23. Database Constraints

Important constraints include:

Candidate skill uniqueness
UNIQUE(candidate_id, skill_id)
Skill normalized name

Canonical skills should prevent duplicate normalized names.

For example:

javascript

should not exist twice as two canonical skills.

24. Initial Seed Data

The MVP should include a small deterministic seed set of common skills.

For example:

JavaScript
TypeScript
Python
Java
C#
C++
HTML
CSS
Angular
React
Vue
Node.js
FastAPI
Express
Django
Spring Boot
MySQL
PostgreSQL
MongoDB
Firebase
AWS
Docker
Git
GitHub
REST API
GraphQL
Redis
Kubernetes

Do not attempt to build a complete global skill taxonomy in Phase 10.7.

The seed data exists only to make the MVP usable.

The seed process must be repeatable and idempotent.

25. Important: Skills Must Not Be Hardcoded in the Frontend

Do not create:

const skills = [
  "JavaScript",
  "Python",
  "Angular"
]

inside Angular components.

Skills belong to backend/database source of truth.

The frontend should retrieve them through the API.

26. Frontend Scope

Create the candidate skills UI.

The candidate should be able to:

Profile
  ↓
Skills
  ↓
Search skill
  ↓
Select skill
  ↓
Set optional proficiency
  ↓
Set optional years of experience
  ↓
Save

The UI should show existing candidate skills.

Example:

Skills

JavaScript       Intermediate
TypeScript       Intermediate
Angular          Intermediate
Python           Beginner

[ + Add Skill ]
27. Skill Search UI

When the user selects:

Add Skill

provide searchable suggestions.

Example:

Search: "java"

Java
JavaScript

The user selects the canonical skill.

Do not create a new skill just because the search text doesn't exactly match.

28. Candidate Skill Editing

The candidate should be able to modify:

Proficiency
Years of experience
Primary status

They should also be able to remove a skill.

29. Primary Skills

is_primary can identify skills the candidate considers important.

Example:

JavaScript → primary
Angular → primary
Python → primary
Docker → not primary

This does not mean the system considers those skills more objectively important.

It is simply candidate preference.

30. Profile Completeness Integration

Phase 10.6 introduced profile completeness.

Phase 10.7 should integrate skills into completeness where appropriate.

For example:

Basic Profile       ✓
Experience          ✓
Education           ✓
Projects            ✓
Skills              ✓

Do not create a candidate quality score.

31. No Matching Yet

Do NOT implement:

Candidate Skill
        ↓
Job Skill
        ↓
Match Score

That belongs to later matching phases.

10.7 only creates the skill foundation.

32. No AI Yet

Do not use Gemini to decide:

"This candidate has JavaScript."

Do not use an LLM for ordinary CRUD or normalization.

AI will later help with:

Skill extraction from resumes
Skill extraction from JDs
Related-skill reasoning
Skill-gap analysis
Semantic matching

Those belong to later phases.

33. Testing
Skill tests

Test:

Create canonical skill
Search skill
Search aliases
Duplicate normalized skill prevention
Candidate skill tests

Test:

Add skill
Update skill
Delete skill
Duplicate candidate skill prevention
Authorization

Test:

Candidate A cannot modify Candidate B's skill.
Validation

Test:

Invalid proficiency
Invalid years
Invalid IDs
Missing required fields
Database

Test:

Foreign keys
Unique constraints
Migration
Seed data
34. API Tests

At minimum:

GET /api/v1/skills

should work without candidate ownership because canonical skills are shared reference data, subject to the application's authentication policy.

Candidate-specific endpoints require authentication:

GET /api/v1/profile/skills
POST /api/v1/profile/skills
PUT /api/v1/profile/skills/{id}
DELETE /api/v1/profile/skills/{id}

Unauthorized requests should return:

401

Attempts to access another candidate's resource should be rejected.

35. Manual Verification

Test the complete flow:

Login
 ↓
Profile
 ↓
Skills
 ↓
Add JavaScript
 ↓
Set Intermediate
 ↓
Save
 ↓
Refresh
 ↓
JavaScript still exists

Then:

Add JavaScript again

should not create a duplicate.

Search:

JS

should be capable of finding:

JavaScript

through the alias.

36. Security

Enforce:

Firebase authentication
Candidate ownership
Backend authorization
Input validation
Database constraints
No secrets in frontend
No direct database access from frontend

Canonical skills are shared reference data, while CandidateSkill records are private candidate-owned data.

37. Definition of Done

Phase 10.7 is complete when:

Database
skills table exists
skill_aliases table exists
candidate_skills table exists
skill_evidence table exists
Constraints exist
Alembic migration works
Seed data works
Backend
Skill search works
Skill alias lookup works
Candidate skill CRUD works
Evidence foundation works
Ownership is enforced
Frontend
Candidate can view skills
Candidate can search skills
Candidate can add skills
Candidate can edit skills
Candidate can remove skills
Testing
Unit tests pass
API tests pass
Authorization tests pass
Database tests pass
Angular build passes
Security
Candidate A cannot manipulate Candidate B's skills
Canonical skills cannot be duplicated through normal operations
38. Non-Goals

Do NOT implement:

Job skills
Job matching
Skill-gap analysis
Resume skill extraction
JD skill extraction
Semantic skill matching
AI skill classification
RAG
Agents
Resume tailoring

Those belong to later phases.

39. Deliverables
Backend
├── Skill model
├── SkillAlias model
├── CandidateSkill model
├── SkillEvidence model
├── Repositories
├── Services
├── Schemas
├── API routes
├── Seed data
├── Alembic migration
└── Tests

Frontend
├── Skills UI
├── Skill search
├── Candidate skill management
├── Typed API service
└── Tests