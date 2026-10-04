Phase 3 — Database Design & ERD
1. Purpose

Phase 3 converts the approved High-Level Design (HLD) into a concrete relational data model.

The goal is to define:

What data the system stores
Which entities exist
How entities are related
Primary keys and foreign keys
Unique constraints
Important indexes
Data ownership
Which data belongs in PostgreSQL, Qdrant, object storage, or Firebase Auth
How the schema supports company-first and location-first job discovery
How the schema supports explainable candidate/job matching
How resumes and tailored resumes are connected to applications
How agent activity and external provider activity are recorded

This phase is intentionally database-focused. Backend implementation and API design are handled in later phases.

2. Database Responsibilities

The system uses different storage technologies for different responsibilities.

Storage	Responsibility
PostgreSQL	Primary business/source-of-truth database
Qdrant	Vector/semantic retrieval
Object Storage	Uploaded resumes and generated documents
Firebase Authentication	User identity and authentication
FastAPI	Business/API layer
Google ADK	Agent orchestration
External providers	Job/company/contact information
Important principle

PostgreSQL is the authoritative source for application state.

Qdrant must never become the source of truth for:

Candidate profile
Job status
Applications
Resume versions
Company records
User preferences
Outreach state

Vectors can be regenerated from PostgreSQL data.

3. Core Domain Areas

The database is divided conceptually into these areas:

Candidate Domain
    ├── Candidate
    ├── Candidate Profile
    ├── Role Profile
    ├── Preferences
    ├── Experience
    ├── Education
    ├── Projects
    └── Skills

Company & Discovery Domain
    ├── Company
    ├── Company Location
    ├── Location
    ├── Hiring Source
    └── Company Hiring Source

Job Domain
    ├── Job
    ├── Job Source
    ├── Job Location
    ├── Job Skill
    └── Job Requirement

Matching Domain
    ├── Job Match
    └── Match Evidence

Resume Domain
    ├── Resume
    ├── Resume Version
    ├── Tailored Resume
    └── Resume Claim

Application Domain
    ├── Application
    ├── Application Event
    ├── Contact
    └── Outreach

Agent & Operations Domain
    ├── Integration
    ├── Search Run
    ├── Agent Run
    ├── Agent Tool Call
    ├── Audit Log
    └── Notification
4. Entity List

The initial PostgreSQL model contains the following major entities.

Candidate

Represents the application user/job seeker.

Important fields:

id
firebase_uid
email
name
phone
created_at
updated_at
status

firebase_uid must be unique.

Firebase handles authentication; PostgreSQL stores application-level candidate data.

Candidate Profile

Stores the candidate's general professional profile.

Examples:

headline
summary
years of experience
current designation
current company
preferred career direction
profile completeness

Relationship:

Candidate 1 ─── 1 CandidateProfile

A candidate should have one primary profile.

Role Profile

A candidate can target different role families.

Examples:

Candidate
   ├── Frontend Developer profile
   ├── Full Stack Developer profile
   ├── Forward Deployed Engineer profile
   └── Python Backend Developer profile

This is important because one master resume/profile should not be forced onto every job.

A role profile can define:

role name
target titles
preferred technologies
relevant skills
relevant experience
preferred seniority
role-specific summary
active/inactive status

Relationship:

Candidate 1 ─── N RoleProfile
Candidate Preference

Stores search and career preferences.

Examples:

preferred locations
remote/hybrid/in-office preference
minimum salary
employment type
preferred industries
preferred role families
willingness to relocate
preferred company size

These preferences influence job discovery and ranking.

5. Experience

Stores verified professional experience.

Fields conceptually include:

company
title
start_date
end_date
description
employment_type
location

Relationship:

Candidate 1 ─── N Experience

Experience is source-of-truth data.

The AI can reframe an experience for a particular JD, but it must not invent an experience.

6. Experience Achievement

Experience descriptions should support individual achievements.

Example:

Experience
    ├── Achievement 1
    ├── Achievement 2
    └── Achievement 3

This allows resume tailoring to select the most relevant verified achievements.

7. Education

Stores:

institution
degree
field
start date
end date
grade/CGPA
description

Relationship:

Candidate 1 ─── N Education
8. Project

Stores candidate projects.

Examples:

Teacher Progress Tracking
Full-stack applications
AI projects
Personal projects

Fields:

name
description
project_type
start_date
end_date
URL
repository URL
verified status

Relationship:

Candidate 1 ─── N Project
9. Skill

Skills are first-class entities.

Examples:

Angular
React
TypeScript
Python
FastAPI
PostgreSQL
Docker
AWS
System Design

A skill should have a normalized identity.

Example:

"Postgres"
"PostgreSQL"
"Postgre SQL"

may map to one canonical skill:

PostgreSQL

Fields:

id
normalized_name
display_name
category
description
10. Skill Alias

Stores alternative names for skills.

Example:

Canonical Skill: PostgreSQL

Aliases:
    Postgres
    Postgre SQL
    PG

This helps normalize job descriptions and candidate profiles.

11. Candidate Skill

Candidate and skill have a many-to-many relationship.

Candidate N ─── N Skill

The join table stores:

candidate_id
skill_id
proficiency
years_used
last_used_at
source
confidence

Example:

Candidate
   |
   +── Angular → advanced
   +── TypeScript → intermediate
   +── FastAPI → intermediate
   +── PostgreSQL → intermediate
12. Skill Evidence

Skill evidence answers:

Why does the system believe this candidate has this skill?

Possible evidence:

experience
project
education
certification
candidate-entered skill
resume

Example:

Skill: FastAPI

Evidence:
    Teacher Progress Tracking
    FastAPI backend
    REST API implementation

This is important for explainable matching.

13. Project Skill

Projects and skills are many-to-many.

Project N ─── N Skill

Example:

Teacher Progress Tracking
    ├── Angular
    ├── TypeScript
    ├── FastAPI
    ├── MySQL
    ├── Docker
    └── AWS
14. Company

Represents a normalized company.

Important fields:

id
name
normalized_name
website
industry
company_size
description
founded_year
status

A company must be independent of individual job postings.

This is important because the product is company-first.

15. Location

Location should be a reusable entity.

Possible hierarchy:

Country
   └── State
        └── City
             └── Area

Example:

India
 └── Karnataka
      └── Bengaluru
           └── HSR Layout

The initial MVP can use normalized text fields.

A later version can introduce PostgreSQL/PostGIS for geographic queries.

16. Company Location

A company may have multiple offices.

Company
   ├── Bengaluru
   ├── Mumbai
   ├── Hyderabad
   └── Pune

Relationship:

Company 1 ─── N CompanyLocation

CompanyLocation can store:

company_id
location_id
office address
office type
latitude/longitude if available
source
verified_at
17. Hiring Source

Represents where a company publishes or is observed hiring.

Examples:

Company Careers
LinkedIn
Naukri
Indeed
Wellfound
Company ATS
User Provided
Other permitted source

The system should not assume that every company uses the same source.

18. Company Hiring Source

This is a many-to-many relationship.

Company N ─── N HiringSource

Example:

Company A
    ├── Company Careers
    ├── LinkedIn
    └── Naukri

Company B
    ├── Company Careers
    └── Wellfound

Important fields:

company_id
hiring_source_id
status
discovery_method
confidence
last_verified_at
last_observed_at

This directly supports the product's company-first strategy.

19. Job

Job is the canonical internal representation of an opening.

Fields conceptually include:

id
company_id
title
normalized_title
description
employment_type
seniority
salary_min
salary_max
currency
application_url
posted_at
expires_at
status
discovered_at
last_seen_at

Relationship:

Company 1 ─── N Job
20. Job Source

One job can be discovered through multiple sources.

Example:

Canonical Job
    ├── Company Careers
    ├── LinkedIn
    └── Naukri

Therefore:

Job 1 ─── N JobSource

JobSource stores:

source
external_job_id
source_url
first_seen_at
last_seen_at
source_status
raw metadata if necessary

This allows the system to preserve where the job was found.

21. Job Location

A job can have multiple valid locations.

Example:

Job
    ├── Bengaluru
    ├── Hyderabad
    └── Remote India

Therefore:

Job N ─── N Location

through job_location.

22. Job Skill

Jobs and skills have a many-to-many relationship.

Job N ─── N Skill

Example:

Frontend Developer Job
    ├── Angular
    ├── TypeScript
    ├── REST API
    └── Git

JobSkill can also store:

required/preferred
importance
extracted_from
confidence
23. Job Requirement

Not every requirement is a simple skill.

Examples:

2+ years experience
Bachelor's degree
Bangalore
Good communication
Immediate joiner
Work from office

Therefore JobRequirement stores normalized requirement information.

Possible categories:

skill
experience
education
location
work_mode
employment
eligibility
other
24. Job Match

Represents candidate-to-job evaluation.

Relationship:

Candidate 1 ─── N JobMatch
Job       1 ─── N JobMatch

A JobMatch may contain:

overall_score
match_status
strong_match_count
partial_match_count
missing_count
eligibility_status
explanation
analyzed_at
matching_model/version

Example:

Job Match

Overall: Strong Match

Strong:
    Angular
    TypeScript
    REST APIs

Partial:
    AWS

Missing:
    Kubernetes

The system should avoid pretending that its score is an official ATS score.

25. Match Evidence

Match evidence explains the result.

Relationship:

JobMatch 1 ─── N MatchEvidence

Example:

Requirement:
    FastAPI

Evidence:
    Teacher Progress Tracking project

Result:
    Strong match

This makes AI decisions inspectable.

26. Resume

Represents a logical resume owned by a candidate.

Examples:

Candidate
    ├── Master Resume
    ├── Frontend Resume
    ├── Full Stack Resume
    └── FDE Resume

Relationship:

Candidate 1 ─── N Resume
27. Resume Version

Every meaningful resume change should create a version.

Resume
   ├── Version 1
   ├── Version 2
   └── Version 3

This provides history and rollback.

A version may contain:

document path
generated text
template
created_at
status
source profile
28. Tailored Resume

A tailored resume is generated specifically for a job.

Relationship:

Job 1 ─── N TailoredResume
Resume 1 ─── N TailoredResume

Example:

Base Resume:
    FDE Resume v4

Target:
    Company A — FDE-1

Tailored Resume:
    FDE-1 Application Resume v1

This prevents overwriting the candidate's base resume.

29. Resume Claim

Every important generated resume claim should be traceable to verified candidate data.

Example:

Resume sentence:
    "Built REST APIs using FastAPI."

Source:
    Project → Teacher Progress Tracking

ResumeClaim can store:

claim text
source entity
source entity ID
verification status

This supports the critical rule:

Never fabricate experience, skills, education, projects, or achievements.

30. Application

Represents an application to a canonical job.

Relationship:

Candidate 1 ─── N Application
Job       1 ─── N Application

Application should reference:

candidate
job
resume/version used
application URL
status
applied_at
notes

Potential statuses:

DISCOVERED
SHORTLISTED
READY
APPLIED
ASSESSMENT
INTERVIEW
REJECTED
WITHDRAWN
OFFER
ACCEPTED
31. Application Event

Application status should have history.

Application
    ├── discovered
    ├── shortlisted
    ├── applied
    ├── interview
    └── rejected

Each event stores:

event type
timestamp
source
notes
actor

This makes application tracking auditable.

32. Contact

Stores public/permitted professional contacts related to companies.

Examples:

recruiter
HR
hiring manager
founder
company contact

Important:

Only collect and store contact information through permitted/public sources or user-provided integrations.

Fields can include:

company_id
name
role
email
LinkedIn URL
source
confidence
verified_at
33. Outreach

Represents generated or sent outreach.

Examples:

HR email
Recruiter email
Founder outreach
LinkedIn message draft

Outreach should track:

recipient
contact
application/job
message content
channel
status
created_at
sent_at
approval status

Initial product rule:

AI generates
      ↓
User reviews
      ↓
User approves
      ↓
Send
34. Integration

Represents connected external services.

Examples:

Gmail
GitHub
permitted job APIs
other supported providers

Store provider metadata, not raw secrets.

Credentials/tokens should be handled through secure secret storage.

35. Search Run

Represents a discovery/search execution.

Example:

Search:
HSR Layout + Frontend + Bangalore

A SearchRun can store:

candidate
search criteria
started_at
completed_at
status
result count
provider summary

This allows the system to explain what happened during discovery.

36. Agent Run

Represents one AI agent execution.

Example:

Career Orchestrator
    ↓
Company Agent
    ↓
Job Discovery Agent
    ↓
Matching Agent

AgentRun stores:

agent name
run ID
parent run
status
started_at
completed_at
model/provider
input reference
output reference
error information

Do not store unnecessary sensitive prompts/responses indefinitely.

37. Agent Tool Call

Tracks tools invoked by an agent.

Example:

Job Discovery Agent
    ↓
CompanyCareerProvider
    ↓
search_jobs()

Useful for debugging and observability.

Fields:

agent_run_id
tool name
provider
arguments metadata
result status
duration
error

Sensitive values must be redacted.

38. Audit Log

Tracks important user/system actions.

Examples:

Resume created
Resume approved
Application submitted
Integration connected
Automation enabled
Application status changed

Audit logs are important for security and troubleshooting.

39. Notification

Stores user notifications.

Examples:

New matching job found
Application status changed
Interview reminder
Resume ready for approval
Agent run failed
40. Main Relationships

The high-level ER relationship looks like:

                         ┌──────────────────┐
                         │     Candidate    │
                         └────────┬─────────┘
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
          ▼                       ▼                        ▼
 CandidateProfile            RoleProfile              Experience
          │                                                │
          │                                                ▼
          │                                      ExperienceAchievement
          │
          ├────────── CandidateSkill ────────── Skill
          │
          ├────────── Project ───────────────── ProjectSkill
          │
          ├────────── Education
          │
          ├────────── Resume ─────────────── ResumeVersion
          │                                      │
          │                                      ▼
          │                               TailoredResume
          │
          └────────── Application ───────── ApplicationEvent
                              │
                              ▼
                             Job
                              │
              ┌───────────────┼─────────────────┐
              │               │                 │
              ▼               ▼                 ▼
           Company       JobSource          JobSkill
              │
        ┌─────┴──────────┐
        ▼                ▼
 CompanyLocation    CompanyHiringSource
        │                │
        ▼                ▼
     Location        HiringSource
41. Candidate-to-Job Matching Relationship

The important matching chain is:

Candidate
    │
    ├── Candidate Skills
    ├── Experience
    ├── Projects
    ├── Education
    └── Role Profile
             │
             ▼
          JobMatch
             │
             ├── MatchEvidence
             │
             ▼
            Job
             │
             ├── JobSkill
             ├── JobRequirement
             └── JobLocation

This allows the system to answer:

Why is this job a good match for me?

instead of only returning:

Match score = 82%.

42. Company-First Discovery Relationship

This product's main differentiator requires a specific relationship:

Candidate Preference
        │
        ▼
     Location
        │
        ▼
    Companies
        │
        ▼
Company Hiring Sources
        │
        ├── Company Careers
        ├── LinkedIn
        ├── Naukri
        ├── Indeed
        └── Wellfound
        │
        ▼
       Jobs
        │
        ▼
    Job Matching

The system should learn/store which hiring sources are useful for each company.

43. Canonical Job and Duplicate Handling

The same job can appear on multiple sources.

Example:

Company Careers
      │
      └── Job ID 123

LinkedIn
      │
      └── Same Job

Naukri
      │
      └── Same Job

These should not automatically become three separate internal jobs.

Instead:

Canonical Job
   ├── JobSource: Company Careers
   ├── JobSource: LinkedIn
   └── JobSource: Naukri

Potential duplicate detection signals:

company
external job ID
normalized title
location
application URL
description similarity
posting timestamps

The system should preserve source records even after canonicalization.

44. Important Constraints
Firebase UID
candidate.firebase_uid UNIQUE

One Firebase identity maps to one candidate.

Skill

Normalized skill names should be unique.

skill.normalized_name UNIQUE
Job Source

A provider's external job identifier should be unique within that provider.

(provider, external_job_id) UNIQUE
Application

Normally one candidate should not create duplicate active applications for the same canonical job.

Potential constraint:

(candidate_id, job_id) UNIQUE

or a controlled uniqueness rule if re-application is allowed.

Role Profile

A candidate should avoid duplicate active role profiles with the same role identity.

45. Foreign Key Strategy

Foreign keys should be used for strong relationships.

Examples:

candidate_profile.candidate_id
    → candidate.id

experience.candidate_id
    → candidate.id

job.company_id
    → company.id

application.job_id
    → job.id

Delete behavior must be deliberate.

For important historical records:

RESTRICT

or soft deletion is often safer than cascading deletion.

For dependent configuration records, controlled cascading may be appropriate.

46. Timestamps

Most operational tables should have:

created_at
updated_at

Event/history tables should generally have:

created_at

External observations should also track:

first_seen_at
last_seen_at

All timestamps should be stored consistently in UTC.

The UI can convert timestamps to the user's local timezone.

47. Soft Delete

Soft delete should not be applied blindly to every table.

It can be useful for:

candidate profiles
companies
jobs
resumes
integrations

But historical events should generally remain immutable.

If soft delete is used:

deleted_at

can be added.

48. JSONB Usage

PostgreSQL JSONB can be used for flexible provider-specific metadata.

Example:

job_source.metadata

However, JSONB must not replace normal relational columns when the application needs to:

search the field
join on it
enforce constraints
report on it
filter frequently

Rule:

Structured business data → relational columns.

Provider-specific flexible metadata → JSONB.

49. Indexing Strategy

Indexes should support real queries.

Important examples:

Candidate
candidate.firebase_uid
candidate.email
Company
company.normalized_name
company.website
Job
job.company_id
job.normalized_title
job.status
job.posted_at
job.last_seen_at
JobSource
(provider, external_job_id)
JobLocation
job_location.job_id
job_location.location_id
CandidateSkill
candidate_skill.candidate_id
candidate_skill.skill_id
JobSkill
job_skill.job_id
job_skill.skill_id
Application
application.candidate_id
application.job_id
application.status
application.applied_at

Indexes should be added based on query patterns rather than indexing every column.

50. Data Ownership

A critical architecture rule:

Candidate data
    → PostgreSQL

Company data
    → PostgreSQL

Job data
    → PostgreSQL

Application state
    → PostgreSQL

Resume metadata
    → PostgreSQL

Resume files
    → Object Storage

Embeddings
    → Qdrant

Authentication identity
    → Firebase Auth
51. Qdrant Relationship

Qdrant does not replace PostgreSQL.

Example:

PostgreSQL
    │
    │ Candidate profile / job / resume content
    ▼
Embedding pipeline
    │
    ▼
Qdrant

Each vector should retain a reference to the PostgreSQL entity.

Example:

vector:
    collection = job_embeddings
    point_id = job_id
    payload:
        entity_type = "job"
        entity_id = "..."

If Qdrant data is lost, vectors can be regenerated.

52. Object Storage Relationship

Resume documents should not be stored directly inside PostgreSQL as large binary data.

Instead:

ResumeVersion
     │
     └── object_storage_key
              │
              ▼
        PDF/DOCX file

PostgreSQL stores metadata.

Object storage stores the actual file.

53. Data Lifecycle Example

A real job discovery flow may look like:

1. User selects HSR Layout.

2. SearchRun is created.

3. Company discovery identifies companies.

4. Company records are created/updated.

5. Hiring sources are discovered.

6. Job providers return openings.

7. Job records are normalized.

8. Duplicate jobs are merged.

9. Job skills and requirements are extracted.

10. Candidate profile is loaded.

11. JobMatch is generated.

12. MatchEvidence explains the result.

13. Correct RoleProfile is selected.

14. ResumeVersion is selected.

15. TailoredResume is generated.

16. User approves.

17. Application is created.

18. ApplicationEvent records the application.

19. Outreach may be generated.

20. Future events update the application history.
54. Why PostgreSQL Instead of Firestore as the Primary Database?

The product contains many relational relationships:

Candidate ↔ Skills
Candidate ↔ Jobs
Company ↔ Locations
Company ↔ Hiring Sources
Job ↔ Sources
Job ↔ Skills
Candidate ↔ Jobs
Applications ↔ Jobs
Applications ↔ Resume Versions

It also needs:

constraints
transactions
joins
reporting
deduplication
historical tracking
consistent application state

PostgreSQL is therefore a better primary source of truth.

Firebase Authentication can still be used because authentication and application data are separate concerns.

55. Example Relational Query Thinking

A user asks:

Show me frontend jobs around HSR Layout that are a strong match.

Conceptually the database needs to combine:

Job
   ↓
Company
   ↓
CompanyLocation / JobLocation
   ↓
Location
   ↓
JobSkill
   ↓
JobMatch
   ↓
Candidate

This is exactly the type of relationship-heavy query where a relational database is useful.

56. Explainability Requirements

The schema must support explanations.

The system should be able to answer:

Why did I match?

Use:

JobMatch
+
MatchEvidence
+
CandidateSkill
+
SkillEvidence
Why was this resume selected?

Use:

RoleProfile
+
Resume
+
ResumeVersion
+
TailoredResume
Why was this company discovered?

Use:

Company
+
CompanyLocation
+
CompanyHiringSource
+
SearchRun
Where did this job come from?

Use:

Job
+
JobSource
57. Agent Observability

The schema also supports debugging AI behavior.

Example:

AgentRun
    │
    ├── AgentToolCall
    ├── AgentToolCall
    └── AgentToolCall

If the Job Discovery Agent returns incorrect jobs, we should be able to inspect:

Which agent ran?
Which provider was called?
Which tool was used?
When?
What was the result?
Did it fail?

This is important because the system is agent-assisted.

58. Security Considerations

Do not store:

plaintext passwords
raw provider secrets
unnecessary access tokens
sensitive personal information without purpose

Use:

Firebase Auth for authentication
secure secret storage for integration credentials
authorization checks in FastAPI
audit logs
least privilege
input validation
provider-specific credential isolation

The database must not trust an LLM-generated user ID or authorization decision.

59. MVP Schema Boundary

For the first usable version, the most important entities are:

candidate
candidate_profile
role_profile
candidate_preference

experience
education
project
skill
candidate_skill
project_skill

company
location
company_location
hiring_source
company_hiring_source

job
job_source
job_location
job_skill
job_requirement

job_match
match_evidence

resume
resume_version
tailored_resume
resume_claim

application
application_event

Advanced operational entities can initially be simplified:

contact
outreach
integration
search_run
agent_run
agent_tool_call
audit_log
notification

But their architectural place should already be defined.

60. Phase 3 Completion Checklist

Phase 3 is complete when:

 Primary database selected: PostgreSQL
 Storage responsibilities defined
 Candidate domain modeled
 Company domain modeled
 Location domain modeled
 Hiring-source domain modeled
 Job domain modeled
 Matching domain modeled
 Resume domain modeled
 Application domain modeled
 Agent/operations domain modeled
 Major relationships defined
 Foreign-key strategy defined
 Unique constraints identified
 Indexing strategy defined
 Duplicate-job strategy defined
 Explainability model defined
 Qdrant relationship defined
 Object-storage relationship defined
 Security considerations documented
 MVP schema boundary defined
61. What We Do NOT Do Yet

Do not start writing SQLAlchemy models yet.

Do not create FastAPI routes yet.

Do not create API endpoints yet.

Do not start coding agents yet.

Do not create Qdrant collections yet.

Do not start scraping providers.

Those belong to later phases.

The next phase is:

Phase 4 — Backend Low-Level Design (LLD)

Phase 4 will convert this database model into:

FastAPI
   │
   ├── routers
   ├── services
   ├── repositories
   ├── schemas
   ├── models
   ├── dependencies
   ├── authentication
   ├── authorization
   ├── error handling
   └── background processing
62. Fixed Development Sequence

We continue in this exact order:

PHASE 0 — Requirements
        │
        ▼
PHASE 1 — Product flows & use cases
        │
        ▼
PHASE 2 — HLD
        │
        ▼
PHASE 3 — Database / ERD ⭐ CURRENT
        │
        ▼
PHASE 4 — Backend LLD
        │
        ▼
PHASE 5 — API contracts
        │
        ▼
PHASE 6 — Agent + Tool + MCP architecture
        │
        ▼
PHASE 7 — RAG / Vector architecture
        │
        ▼
PHASE 8 — Security
        │
        ▼
PHASE 9 — Project setup
        │
        ▼
PHASE 10 — Build MVP feature-by-feature
        │
        ▼
PHASE 11 — Testing + evaluation
        │
        ▼
PHASE 12 — Deployment
63. Learning Objective

This phase teaches an important software-engineering skill:

Before writing backend code, understand what information the product owns, how that information is related, where it is stored, and what rules protect its consistency.

The database is not merely a collection of tables.

It represents the business model of the product.

For this application, the central business model is:

Candidate
    ↓
Preferences
    ↓
Locations
    ↓
Companies
    ↓
Hiring Sources
    ↓
Jobs
    ↓
Matching
    ↓
Resume Selection
    ↓
Tailoring
    ↓
Application
 ↓
Outreach / Tracking