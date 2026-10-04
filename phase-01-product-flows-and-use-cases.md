# Phase 1 — Product Flows & Use Cases

**Project:** AI Career & Job-Hunting Agent  
**Phase:** 1 of 12  
**Status:** Draft v1.0  
**Previous Phase:** Phase 0 — Requirements  
**Next Phase:** Phase 2 — High-Level Design (HLD)

---

# 1. Purpose of This Document

This document converts the Phase 0 product requirements into concrete user flows and use cases.

The purpose is to answer:

- Who uses the system?
- What can the user do?
- What happens step by step?
- What information enters the system?
- What information is produced?
- Which parts are normal application logic?
- Which parts may require AI/agents?
- Which actions require user approval?
- What data relationships will later be required in the database?
- What system boundaries will later influence the HLD?

This document is deliberately written before the HLD and database design.

The sequence is:

```text
Requirements
    ↓
Product Flows & Use Cases   ← THIS DOCUMENT
    ↓
HLD
    ↓
Database / ERD
    ↓
Backend LLD
    ↓
API Contracts
    ↓
Agent + Tool + MCP
    ↓
RAG / Vector
    ↓
Security
    ↓
Project Setup
    ↓
MVP
    ↓
Testing
    ↓
Deployment
```

---

# 2. Product Mental Model

The product should be understood as a career/job-search workflow rather than a collection of unrelated AI features.

The central lifecycle is:

```text
Candidate
   ↓
Candidate Knowledge
   ↓
Career Preferences
   ↓
Location / Company Discovery
   ↓
Hiring Source Discovery
   ↓
Job Discovery
   ↓
Job Understanding
   ↓
Candidate ↔ Job Matching
   ↓
Resume/Profile Selection
   ↓
Job-Specific Resume Tailoring
   ↓
Candidate Review
   ↓
Application / Outreach
   ↓
Application Tracking
   ↓
Feedback / Analysis
   ↓
Improved Future Search
```

The candidate remains the owner and decision-maker for important actions.

---

# 3. Main Actors

## 3.1 Candidate

The primary user.

The candidate can:

- Create an account
- Build a master profile
- Upload resumes
- Maintain role profiles
- Select career interests
- Select target locations
- Discover companies
- Discover jobs
- Review matches
- Generate tailored resumes
- Generate outreach
- Approve applications
- Track applications
- Ask the career chatbot questions
- Connect supported integrations
- Review skill gaps

---

## 3.2 AI Career System

The system coordinates:

- Candidate data
- Company discovery
- Hiring-source intelligence
- Job discovery
- Job normalization
- JD analysis
- Candidate-job matching
- Resume tailoring
- Outreach generation
- Application assistance
- Search history

The AI system must operate within defined tools and permissions.

---

## 3.3 External Job Source

A job source may be:

- Company careers page
- Official job API
- Permitted third-party job provider
- Supported job portal integration
- User-provided job URL
- Other permitted source

The system must not assume unrestricted scraping access.

---

## 3.4 Company

A company is a first-class entity in the product.

The system may discover:

- Company identity
- Official website
- Careers page
- Locations
- Industry
- Hiring sources
- Jobs
- Public/permitted contact information

---

## 3.5 Recruiter / Hiring Contact

A recruiter, HR contact, hiring manager, founder, or other public/permitted contact may become associated with a company or application.

The system should not assume that every company has an available contact.

---

# 4. Core Product Flows

The major flows are:

```text
FLOW 01 — Registration & Onboarding
FLOW 02 — Master Candidate Profile
FLOW 03 — Resume Upload & Parsing
FLOW 04 — Role Profile Creation
FLOW 05 — Location & Career Preference Setup
FLOW 06 — Company Discovery
FLOW 07 — Hiring Source Discovery
FLOW 08 — Job Discovery
FLOW 09 — Job Normalization & Deduplication
FLOW 10 — Job Description Analysis
FLOW 11 — Candidate ↔ Job Matching
FLOW 12 — Resume Selection
FLOW 13 — Resume Tailoring
FLOW 14 — Resume Claim Validation
FLOW 15 — Company / Recruiter Research
FLOW 16 — Outreach Generation
FLOW 17 — Application Assistance
FLOW 18 — Application Tracking
FLOW 19 — Chat / Career Assistant
FLOW 20 — Skill Gap Analysis
FLOW 21 — Search Feedback & Learning
FLOW 22 — Scheduled Job Discovery
FLOW 23 — Integration Connection
```

Not all flows need to be implemented in the first MVP.

---

# 5. Flow 01 — Registration & Onboarding

## Goal

Create the user's account and initialize a candidate record.

## Flow

```text
Candidate
   ↓
Sign Up / Sign In
   ↓
Firebase Authentication
   ↓
Backend verifies identity
   ↓
Candidate record created/found
   ↓
Onboarding
   ↓
Dashboard
```

## Input

- Email / authentication identity
- Name where available
- Authentication provider

## System Actions

1. Authenticate user.
2. Verify identity token.
3. Obtain stable external identity ID.
4. Find candidate record.
5. Create candidate if it does not exist.
6. Start onboarding state.

## Output

A candidate account with an internal candidate ID.

## Important Design Rule

Firebase UID is an identity identifier.

The candidate's application data remains in PostgreSQL.

---

# 6. Flow 02 — Master Candidate Profile

## Goal

Create the source of truth for the candidate.

## Flow

```text
Candidate
   ↓
Enter / Import Information
   ↓
Validate
   ↓
Master Profile
```

## Candidate Information

### Personal

- Name
- Email
- Phone
- Current location
- Links

### Education

- Institution
- Degree
- Field
- Dates
- Grade where relevant

### Experience

- Company
- Role
- Start date
- End date
- Responsibilities
- Achievements

### Projects

- Project name
- Description
- Technologies
- Responsibilities
- Outcomes
- Links

### Skills

- Skill
- Category
- Evidence
- Proficiency where available

### Certifications

- Certification
- Issuer
- Date
- Credential

### Achievements

- Achievement
- Evidence
- Date

## Important Rule

The master profile contains facts.

AI may help organize or extract information, but it should not silently create facts.

---

# 7. Flow 03 — Resume Upload & Parsing

## Goal

Allow the candidate to provide an existing resume and use it to initialize structured profile information.

## Flow

```text
Upload PDF/DOCX
      ↓
Store Original File
      ↓
Extract Text
      ↓
Parse Resume
      ↓
Structured Candidate Data
      ↓
Candidate Review
      ↓
Save Verified Information
```

## Input

- PDF
- DOCX

## Processing

1. Validate file type.
2. Store original file.
3. Extract text.
4. Parse sections.
5. Extract candidate entities.
6. Present extracted information.
7. Candidate confirms or edits.
8. Save verified information.

## Important Rule

Extracted information should not automatically override previously verified information.

---

# 8. Flow 04 — Role Profile Creation

## Goal

Allow the candidate to represent themselves differently for different career directions without duplicating their source-of-truth data.

## Example

```text
Master Profile
      │
      ├── Frontend Profile
      ├── Full Stack Profile
      ├── Backend Profile
      └── FDE Profile
```

## Flow

```text
Master Profile
   ↓
Select Target Role
   ↓
Select Relevant Experience / Skills / Projects
   ↓
Create Role Profile
   ↓
Candidate Reviews
   ↓
Save
```

## Example

A Full Stack profile may emphasize:

```text
Angular
TypeScript
FastAPI
MySQL
Docker
AWS
REST APIs
```

An FDE profile may emphasize:

```text
Requirements gathering
HLD
LLD
Data modeling
Client-facing work
Deployment
Debugging
Solution implementation
```

The underlying facts remain connected to the master profile.

---

# 9. Flow 05 — Location & Career Preferences

## Goal

Tell the system what opportunities the candidate is interested in.

## Candidate Preferences

### Career

- Domain
- Target roles
- Experience level
- Industries
- Skills of interest

### Location

- Country
- State
- City
- Area
- Radius
- Remote
- Hybrid
- On-site

### Company

- Company size
- Industry
- Startup / established company
- Preferred company characteristics

### Compensation

- Minimum salary
- Desired salary
- Currency

## Example

```text
Domain:
Software Engineering

Roles:
Full Stack
Frontend
FDE

Location:
HSR Layout, Bengaluru

Radius:
10 km

Work mode:
On-site / Hybrid

Experience:
1–3 years
```

---

# 10. Flow 06 — Company Discovery

## Goal

Discover relevant companies around a candidate-selected location.

## Example

Candidate selects:

```text
HSR Layout, Bengaluru
10 km radius
Software / Technology
Full Stack / FDE
```

The system:

```text
Location
   ↓
Company Discovery Sources
   ↓
Candidate-Relevant Companies
   ↓
Company Normalization
   ↓
Company Records
```

## Company Data

Potential information:

- Name
- Website
- Official domain
- Industry
- Location
- Company size
- Description
- Careers page
- Discovery source
- Verification timestamp

## Important Rule

A company discovered from one source should not automatically be treated as verified.

The system should track source and verification.

---

# 11. Flow 07 — Hiring Source Discovery

## Goal

Determine where a specific company appears to hire.

This is a core differentiator of the product.

## Flow

```text
Company
   ↓
Official Website
   ↓
Careers Page
   ↓
Permitted Hiring Sources
   ↓
Source Verification
   ↓
Company ↔ Hiring Source Relationship
```

## Example

```text
Company X
│
├── Official Careers Page
│       Status: Active
│
├── LinkedIn
│       Status: Observed
│
├── Naukri
│       Status: Observed
│
└── Indeed
        Status: Not Recently Observed
```

## Stored Information

For the company/source relationship:

- Source
- Status
- Last observed
- Last verified
- Discovery method
- Confidence where useful

This allows the system to learn that companies use different hiring channels.

---

# 12. Flow 08 — Job Discovery

## Goal

Find current jobs from supported sources.

## Flow

```text
Company
   ↓
Known Hiring Sources
   ↓
Provider Calls
   ↓
Raw Job Data
   ↓
Normalization
   ↓
Canonical Job
```

## Job Search Inputs

- Role
- Skills
- Company
- Location
- Radius
- Work mode
- Experience
- Domain
- Date/freshness

## Example

```text
Find:
Full Stack / FDE

Around:
HSR Layout

Companies:
Company A, B, C

Experience:
1–3 years
```

---

# 13. Flow 09 — Job Normalization & Deduplication

## Problem

The same job may appear in multiple sources.

```text
Company Careers
       │
LinkedIn ─────┐
       │      │
Naukri ───────┼──> Same underlying job
       │      │
Indeed ───────┘
```

## Flow

```text
Raw Job
   ↓
Normalize Fields
   ↓
Find Possible Existing Job
   ↓
Compare Identifiers / Content
   ↓
Duplicate?
 ┌───────┴────────┐
Yes               No
 ↓                 ↓
Link Source      Create Job
```

## Important Principle

Do not throw away source information.

Instead:

```text
Canonical Job
   ├── Company Careers source
   ├── LinkedIn source
   └── Naukri source
```

This preserves where the job was observed.

---

# 14. Flow 10 — Job Description Analysis

## Goal

Convert an unstructured JD into structured requirements.

## Flow

```text
Job Description
      ↓
JD Parser
      ↓
Structured Requirements
      ↓
Skills
Responsibilities
Experience
Education
Location
Work Mode
Employment Type
      ↓
Store
```

## Example

Raw JD:

```text
Looking for a Full Stack Engineer with experience
in Angular, Python, REST APIs and SQL...
```

Structured result:

```text
Role:
Full Stack Engineer

Required:
Angular
Python
REST APIs
SQL

Experience:
1–3 years

Location:
Bengaluru
```

---

# 15. Flow 11 — Candidate ↔ Job Matching

## Goal

Determine how the candidate relates to the job using evidence.

## Flow

```text
Job
 ↓
JD Requirements
 ↓
Candidate Profile
 ↓
Relevant Candidate Evidence
 ↓
Comparison
 ↓
Match Analysis
```

## Match Categories

### Strong Match

Candidate has verified evidence.

### Partial Match

Candidate has related experience but not exact evidence.

### Missing

Requirement is not represented in the candidate's verified information.

### Not Verified

The candidate may have the capability, but the system has no reliable evidence.

### Eligibility Issue

Example:

- Required experience clearly outside candidate's range
- Location restriction
- Required qualification

## Output

```text
Skill                Result       Evidence
------------------------------------------------
Angular              Strong       Project A
FastAPI              Strong       Project B
Docker               Strong       Project B
Kubernetes           Missing      No evidence
AWS                  Partial      EC2/S3 experience
```

The system should explain the evidence instead of presenting only one opaque score.

---

# 16. Flow 12 — Resume Selection

## Goal

Choose the correct base role profile/resume before tailoring.

## Flow

```text
Job
 ↓
Classify Role
 ↓
Compare Role Profiles
 ↓
Select Best-Matching Base Profile
 ↓
Tailoring
```

## Example

```text
Job:
Frontend Engineer

Available:
Frontend Profile
Full Stack Profile
FDE Profile

Selected:
Frontend Profile
```

Another:

```text
Job:
Forward Deployed Engineer

Selected:
FDE Profile
```

The selection should be explainable.

---

# 17. Flow 13 — Resume Tailoring

## Goal

Generate a job-specific resume from verified candidate information.

## Flow

```text
Job
 ↓
Selected Role Profile
 ↓
Relevant Candidate Evidence
 ↓
Resume Tailoring
 ↓
Draft Resume
```

## Allowed

- Reorder skills
- Reorder projects
- Rewrite truthful bullet points
- Improve wording
- Highlight relevant experience
- Align terminology
- Change summary
- Select relevant achievements

## Not Allowed

- Invent a technology
- Invent a project
- Invent employment
- Invent achievement
- Invent certification
- Invent years of experience
- Claim unsupported responsibilities

---

# 18. Flow 14 — Resume Claim Validation

## Goal

Validate that the generated resume remains grounded in candidate data.

## Flow

```text
Generated Resume
      ↓
Extract Claims
      ↓
Compare With Master Profile
      ↓
Evidence Check
      ↓
Valid / Needs Review
      ↓
Candidate Review
```

## Example

Generated claim:

```text
"Built production Kubernetes infrastructure."
```

Candidate evidence:

```text
No Kubernetes experience found.
```

Result:

```text
UNSUPPORTED CLAIM
```

The system must flag it rather than silently retaining it.

---

# 19. Flow 15 — Company / Recruiter Research

## Goal

Collect useful company information before application/outreach.

## Flow

```text
Company
 ↓
Official Website
 ↓
Careers Information
 ↓
Public/Permitted Company Information
 ↓
Relevant Contacts Where Available
 ↓
Company Research Summary
```

## Possible Information

- Company description
- Products
- Industry
- Hiring patterns
- Relevant teams
- Careers page
- Public/permitted recruiter information
- Public/permitted contact information

The system should clearly distinguish verified facts from generated interpretation.

---

# 20. Flow 16 — Outreach Generation

## Goal

Prepare personalized communication.

## Flow

```text
Job
 ↓
Company
 ↓
Available Contact
 ↓
Candidate Profile
 ↓
Relevant Evidence
 ↓
Outreach Draft
 ↓
Candidate Review
 ↓
Send if approved
```

## Possible Targets

- Recruiter
- HR
- Hiring manager
- Founder
- Company contact

The target depends on company context and available information.

## Important Rule

Initial implementation should generate drafts, not silently send messages.

---

# 21. Flow 17 — Application Assistance

## Goal

Help the candidate submit a job application.

## Flow

```text
Job
 ↓
Candidate Match
 ↓
Resume Selection
 ↓
Resume Tailoring
 ↓
Application Data Preparation
 ↓
Candidate Review
 ↓
Approval
 ↓
Application
```

## Application Status

```text
Discovered
Reviewed
Shortlisted
Resume Prepared
Ready to Apply
Applied
Recruiter Contacted
Interview
Offer
Rejected
Withdrawn
Closed
```

---

# 22. Flow 18 — Application Tracking

## Goal

Maintain a complete history.

## Flow

```text
Application
   ↓
Events
   ├── Applied
   ├── Email Sent
   ├── Recruiter Reply
   ├── Interview
   ├── Follow-up
   ├── Rejected
   └── Offer
```

## Important Principle

Do not store only the current status.

The system should preserve the application event history.

---

# 23. Flow 19 — Chat / Career Assistant

## Goal

Provide a conversational interface to the product's capabilities.

## Example Queries

```text
"Find frontend jobs around HSR."

"Which companies near me hire FDEs?"

"Why is this job a partial match?"

"Which resume should I use?"

"Create a resume for this job."

"What skills am I missing?"

"Show my applications from this week."

"Which companies have I not contacted yet?"
```

## Chat Architecture Concept

```text
User
 ↓
Chat API
 ↓
Intent / Task Understanding
 ↓
Relevant Tool or Agent
 ↓
Application Data / Retrieval
 ↓
Response
```

The chatbot should use real application data.

It should not pretend to know the user's current applications or profile from general model knowledge.

---

# 24. Flow 20 — Skill Gap Analysis

## Goal

Identify skills that repeatedly appear in relevant jobs but are missing or weak in the candidate profile.

## Flow

```text
Relevant Jobs
      ↓
Aggregate Requirements
      ↓
Compare Candidate Skills
      ↓
Repeated Gaps
      ↓
Skill Gap Report
```

## Example

```text
Target roles:
Full Stack / FDE

Frequently requested:
Docker       ✓
REST APIs    ✓
FastAPI      ✓
AWS          △
Kubernetes   ✗
Redis        ✗
```

The system can later recommend learning resources.

---

# 25. Flow 21 — Search Feedback & Learning

## Goal

Improve future discovery based on explicit candidate feedback and observed behavior.

## Candidate Feedback

The candidate may say:

```text
Not interested
Wrong role
Too far
Salary too low
Wrong industry
Already applied
Company not interested
```

The system can use this information to improve future filtering.

## Important Rule

User preferences should remain explicit and editable.

The system should not silently infer sensitive personal attributes.

---

# 26. Flow 22 — Scheduled Job Discovery

## Goal

Periodically search for new relevant opportunities.

## Flow

```text
Candidate Preferences
       ↓
Scheduled Search
       ↓
Company / Job Providers
       ↓
Normalize
       ↓
Deduplicate
       ↓
Match
       ↓
New Relevant Jobs
       ↓
Notification
```

Example:

```text
Every morning

Search:
Full Stack / FDE

Location:
Bengaluru

Experience:
1–3 years

Notify:
Only new jobs not previously shown
```

Scheduling is a later MVP phase rather than a Day 1 requirement.

---

# 27. Flow 23 — Integration Connection

## Goal

Allow optional external integrations.

Potential integrations:

```text
GitHub
Email
Supported professional-profile data
Job providers
Storage
```

## Generic Flow

```text
Candidate
 ↓
Connect Integration
 ↓
Authorization
 ↓
Credential / Token Storage
 ↓
Integration Provider
 ↓
Sync
 ↓
Candidate Data / Tool
```

Credentials must not be exposed to agents unnecessarily.

---

# 28. Cross-Flow Data Relationships

The flows reveal the main domain relationships.

```text
Candidate
   │
   ├── Candidate Profile
   │
   ├── Role Profiles
   │
   ├── Skills
   │
   ├── Experience
   │
   ├── Projects
   │
   ├── Resumes
   │
   └── Applications
             │
             ▼
            Job
             │
             ▼
          Company
             │
             ├── Locations
             │
             └── Hiring Sources
                         │
                         ▼
                    Job Sources
```

These relationships will directly inform Phase 3 — Database / ERD.

---

# 29. Normal User Journey

A normal candidate journey should look like:

```text
1. Sign up
      ↓
2. Build profile
      ↓
3. Upload resume
      ↓
4. Confirm extracted information
      ↓
5. Select target roles
      ↓
6. Select locations
      ↓
7. Discover companies
      ↓
8. Discover hiring sources
      ↓
9. Discover jobs
      ↓
10. Review matches
      ↓
11. Open a job
      ↓
12. See match explanation
      ↓
13. Select recommended role profile
      ↓
14. Generate tailored resume
      ↓
15. Review resume
      ↓
16. Generate outreach if appropriate
      ↓
17. Apply
      ↓
18. Track application
```

---

# 30. Alternative User Journey — User Already Has a Job URL

The user should not be forced to go through company discovery.

```text
Paste Job URL
     ↓
Fetch / Import Job
     ↓
Normalize
     ↓
Analyze JD
     ↓
Match Candidate
     ↓
Select Resume
     ↓
Tailor
     ↓
Apply / Track
```

This is important because the platform must support both:

```text
Discovery-first
```

and:

```text
Job-first
```

workflows.

---

# 31. Alternative User Journey — Company-First

A candidate may already have a company in mind.

```text
Search Company
      ↓
Company Profile
      ↓
Hiring Sources
      ↓
Current Jobs
      ↓
Candidate Match
      ↓
Resume
      ↓
Application
```

This is especially important for the product's company-first strategy.

---

# 32. Alternative User Journey — Career Exploration

A candidate may not know the exact job title.

Example:

```text
"I know I like frontend, backend and working
directly with customers, but I don't know
which roles to search for."
```

The system can:

```text
Candidate Interests
      ↓
Role Taxonomy
      ↓
Possible Role Families
      ↓
Explain Differences
      ↓
Candidate Selects Interests
      ↓
Search
```

The system should inform the candidate rather than make an irreversible career decision for them.

---

# 33. Error / Exception Flows

## Job Source Unavailable

```text
Provider
 ↓
Failure
 ↓
Log failure
 ↓
Mark source unavailable
 ↓
Continue other providers
```

The entire job search should not fail because one provider is unavailable.

---

## Company Careers Page Unavailable

```text
Company
 ↓
Careers page unavailable
 ↓
Use other permitted sources
 ↓
Mark careers source unavailable/stale
```

---

## Duplicate Company

```text
Company Candidate A
Company Candidate B
      ↓
Entity Matching
      ↓
Possible Duplicate
      ↓
Merge / Review
```

Automatic merging should be conservative.

---

## Duplicate Job

```text
Job A
Job B
      ↓
Duplicate Detection
      ↓
Same Canonical Job
      ↓
Attach Both Sources
```

---

## Resume Unsupported Claim

```text
Tailored Resume
      ↓
Claim Validation
      ↓
Unsupported Claim
      ↓
Flag
      ↓
Fix / Remove
```

---

## Application Submission Failure

```text
Submit
  ↓
Failure
  ↓
Application remains "Ready to Apply"
  ↓
Record failure
  ↓
Allow retry
```

---

# 34. Approval Boundaries

The following should initially be automatic:

```text
Parse resume
Normalize jobs
Deduplicate jobs
Analyze JD
Calculate match evidence
Generate draft resume
Generate outreach draft
```

The following should initially require candidate approval:

```text
Final resume
Send outreach
Submit application
Connect sensitive integration
Enable automated application rules
```

---

# 35. What Requires an Agent?

Not every flow needs an agent.

## Normal Application Logic

Good candidates for deterministic code:

```text
Create candidate
Get candidate
Create application
Update application
Filter by location
Check application duplicate
Save resume metadata
```

## AI / Agentic Work

Good candidates:

```text
Analyze JD
Research company
Find relevant candidate evidence
Explain fit
Tailor resume
Generate outreach
Analyze skill gaps
Coordinate multi-step job search
```

This separation is important for reliability.

---

# 36. What Requires RAG?

Potential RAG use cases:

```text
JD
 ↓
Retrieve relevant candidate projects
 ↓
Retrieve relevant experience
 ↓
Retrieve relevant skills/evidence
 ↓
LLM
```

Another:

```text
Company
 ↓
Retrieve previous company research
 ↓
Current job
 ↓
Candidate context
 ↓
Outreach generation
```

RAG should retrieve information that exists in the system.

It should not be used as a replacement for SQL queries.

---

# 37. What Requires SQL?

Examples:

```text
Find all active jobs in Bengaluru.

Find jobs from companies within the candidate's target area.

Find applications where status = interview.

Find jobs the candidate has not applied to.

Find companies using a specific hiring source.

Find all jobs requiring a particular skill.
```

These are structured database operations.

---

# 38. What Requires Vector Search?

Examples:

```text
Find candidate projects semantically related to this JD.

Find previous experience relevant to this responsibility.

Find jobs similar to a candidate's preferred opportunities.

Find related skill concepts.
```

These are semantic retrieval operations.

---

# 39. Phase 1 Functional Use-Case Table

| ID | Use Case | Primary Actor | Initial Priority |
|---|---|---|---|
| UC-001 | Register/Login | Candidate | MVP |
| UC-002 | Create Master Profile | Candidate | MVP |
| UC-003 | Upload Resume | Candidate | MVP |
| UC-004 | Parse Resume | System | MVP |
| UC-005 | Create Role Profile | Candidate | MVP |
| UC-006 | Set Career Preferences | Candidate | MVP |
| UC-007 | Set Location Preferences | Candidate | MVP |
| UC-008 | Discover Companies | System | MVP |
| UC-009 | Discover Hiring Sources | System | MVP/Core Differentiator |
| UC-010 | Discover Jobs | System | MVP |
| UC-011 | Normalize Job | System | MVP |
| UC-012 | Deduplicate Job | System | MVP |
| UC-013 | Analyze JD | AI | MVP |
| UC-014 | Match Candidate to Job | AI | MVP |
| UC-015 | Select Resume | System/AI | MVP |
| UC-016 | Tailor Resume | AI | MVP |
| UC-017 | Validate Resume Claims | AI/System | MVP |
| UC-018 | Generate Outreach | AI | MVP |
| UC-019 | Apply | Candidate/System | MVP |
| UC-020 | Track Application | Candidate/System | MVP |
| UC-021 | Chat Assistant | AI | MVP |
| UC-022 | Skill Gap Analysis | AI | Later MVP |
| UC-023 | Scheduled Search | System | Later |
| UC-024 | GitHub Integration | System | Later |
| UC-025 | Email Integration | System | Later |
| UC-026 | Controlled Auto-Apply | System | Later |

---

# 40. MVP Boundary

The first MVP should focus on the following end-to-end journey:

```text
Candidate
   ↓
Profile
   ↓
Resume
   ↓
Role Preferences
   ↓
Location
   ↓
Company Discovery
   ↓
Job Discovery
   ↓
JD Analysis
   ↓
Candidate Match
   ↓
Correct Resume
   ↓
Tailored Resume
   ↓
Application Tracking
```

The system should be useful before advanced automation is added.

---

# 41. What Phase 1 Gives Us

This phase establishes the business workflow.

It tells us:

### Entities we need

```text
Candidate
Profile
Role Profile
Experience
Education
Project
Skill
Company
Company Location
Hiring Source
Company Hiring Source
Job
Job Source
Resume
Resume Version
Match Analysis
Application
Application Event
Contact
Outreach
Integration
```

### Relationships we need

```text
Candidate → Profiles
Candidate → Skills
Candidate → Resumes
Candidate → Applications

Company → Jobs
Company → Hiring Sources

Job → Sources
Job → Skills

Candidate ↔ Job → Match

Application → Job
Application → Resume
Application → Events
```

These will be converted into an actual ERD in Phase 3.

---

# 42. Questions Phase 2 Must Answer

The HLD must now answer:

1. What are the major application components?
2. Where does Angular communicate?
3. Where does FastAPI sit?
4. Where does PostgreSQL sit?
5. Where does Qdrant sit?
6. Where does object storage sit?
7. Where does Firebase Authentication sit?
8. Where does Google ADK sit?
9. Where do tools sit?
10. Where does MCP sit?
11. Where do job-source providers sit?
12. How does a job move from an external source into PostgreSQL?
13. How does candidate data move into the matching system?
14. How does RAG participate?
15. How do applications get tracked?
16. Where are approvals enforced?
17. How are external failures isolated?

---

# 43. Phase 1 Completion Criteria

Phase 1 is complete when:

- [x] Main actors are defined.
- [x] Main product flows are defined.
- [x] Candidate onboarding flow is defined.
- [x] Master profile flow is defined.
- [x] Resume flow is defined.
- [x] Role profile flow is defined.
- [x] Location-first discovery flow is defined.
- [x] Company-first flow is defined.
- [x] Hiring-source discovery flow is defined.
- [x] Job discovery flow is defined.
- [x] Job normalization is defined.
- [x] Job deduplication is defined.
- [x] JD analysis is defined.
- [x] Candidate-job matching is defined.
- [x] Resume selection is defined.
- [x] Resume tailoring is defined.
- [x] Claim validation is defined.
- [x] Outreach flow is defined.
- [x] Application flow is defined.
- [x] Tracking flow is defined.
- [x] Chat flow is defined.
- [x] AI vs deterministic responsibilities are identified.
- [x] SQL vs vector-search responsibilities are identified.
- [x] Main entities and relationships are identified.
- [x] MVP boundary is defined.

---

# 44. Transition to Phase 2

The next phase is:

> **Phase 2 — High-Level Design (HLD)**

Phase 2 will take the workflows in this document and convert them into the system architecture.

The key transformation will be:

```text
Product Flow
     ↓
System Components
     ↓
Component Responsibilities
     ↓
Communication
     ↓
Data Flow
     ↓
External Integrations
```

The HLD will be created as a separate document:

```text
docs/02-hld.md
```

It will not repeat this document unnecessarily.

It will explain **how the system technically supports these flows**.

---

# 45. Learning Objective

By completing Phase 1, the developer should understand:

- What a product flow is
- What a use case is
- Difference between actor and system
- Difference between business logic and AI logic
- Why approval boundaries matter
- Why source-of-truth data matters
- Why job portals should be provider-based
- Why duplicate jobs need canonicalization
- Why company and hiring source are separate entities
- Why one candidate can have multiple role profiles
- Why one job can have multiple source records
- Why SQL and vector search solve different problems
- How product requirements become technical architecture

This understanding should be established before writing the HLD.
