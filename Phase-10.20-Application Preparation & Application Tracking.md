# Phase 10.20 — Application Preparation & Application Tracking

## 1. Objective

Build the application domain that allows a candidate to take a discovered job, review the selected/tailored resume, prepare application information, and create an application record.

The system must preserve:

- which job was applied to
- which resume was used
- which resume version was used
- which role profile was used
- when the application happened
- where the application happened
- application status
- application events
- candidate notes
- outreach relationship where applicable

Pipeline:

Job
↓
Candidate Match
↓
Resume Selection
↓
Resume Tailoring
↓
Application Preparation
↓
Candidate Approval
↓
Application
↓
Application Tracking

---

# 2. Critical Boundary

This phase is NOT:

- unrestricted auto-apply
- mass application bot
- browser automation across arbitrary websites
- CAPTCHA bypass
- credential sharing
- automatic LinkedIn/Naukri account control
- automatic submission without candidate approval

The initial system must use:

Candidate
+
Approved application workflow

The candidate remains in control of submission.

---

# 3. Product Goal

The system should answer:

"What jobs have I applied to, with which resume, when, and what happened afterward?"

Example:

Application:

Company:
Example Technologies

Job:
Forward Deployed Engineer

Resume:
FDE Resume v3

Tailored Resume:
Tailored Resume #17

Application URL:
Company Careers

Applied:
04 Oct 2026

Status:
Applied

Events:
04 Oct → Applied
08 Oct → Recruiter Email
15 Oct → Interview
20 Oct → Rejected

---

# 4. Application vs Job

A Job represents an opportunity.

An Application represents the candidate's action against that opportunity.

One candidate may have:

Job
    ↓
Application

Another candidate may have:

Same Job
    ↓
Application

Therefore:

Job != Application

---

# 5. Relationship

Use:

Candidate
    ↓
Application
    ↓
Job

Application also references:

- Resume
- Resume Version
- Tailored Resume
- Role Profile

---

# 6. Database

Reuse the planned:

applications
application_events

domain if it already exists.

Do not create duplicate tables if implementation already exists.

If not implemented, create:

applications

Suggested fields:

id
candidate_id
job_id
resume_id
resume_version_id
tailored_resume_id
role_profile_id
application_url
application_method
status
applied_at
source
candidate_notes
created_at
updated_at

---

# 7. Application Status

Use controlled statuses.

Recommended:

DRAFT
READY
APPLIED
UNDER_REVIEW
RECRUITER_CONTACTED
INTERVIEWING
OFFER
ACCEPTED
REJECTED
WITHDRAWN
CLOSED
UNKNOWN

Do not allow arbitrary status strings.

---

# 8. Application Method

Examples:

official_company_site
job_board
referral
email
recruiter
user_provided
other

Future integrations can add provider-specific methods.

---

# 9. Application Source

Preserve where the job/application came from.

Examples:

company_careers
linkedin
naukri
indeed
wellfound
user_provided
referral
other

The system must not assume that a source is allowed to be automated.

---

# 10. Application Events

Create/reuse:

application_events

Suggested fields:

id
application_id
event_type
event_at
source
notes
metadata
created_at

---

# 11. Event Types

Recommended:

CREATED
READY
APPLIED
STATUS_CHANGED
RECRUITER_CONTACTED
INTERVIEW_SCHEDULED
INTERVIEW_COMPLETED
OFFER_RECEIVED
REJECTED
WITHDRAWN
NOTE_ADDED

Future event types may be added through controlled enums.

---

# 12. Event History

Never overwrite important historical events.

Example:

Application status:

APPLIED

Event history:

04 Oct:
CREATED

04 Oct:
READY

04 Oct:
APPLIED

08 Oct:
RECRUITER_CONTACTED

15 Oct:
INTERVIEW_SCHEDULED

20 Oct:
REJECTED

This history is important for later analytics.

---

# 13. Application Preparation

Before application creation, verify:

- job still exists
- job is not clearly expired
- candidate owns the job context
- selected resume exists
- selected resume version exists
- tailored resume exists if candidate chose to tailor
- tailored resume is not stale
- application URL exists where required
- candidate has reviewed the application

---

# 14. Resume Requirement

An application should record exactly which resume was used.

Possible:

resume_id

resume_version_id

tailored_resume_id

This is important because the candidate may later change their resume.

Historical application data must not change.

---

# 15. Historical Integrity

Suppose:

Application A

used:

FDE Resume v3

Later candidate uploads:

FDE Resume v4

Application A must still show:

FDE Resume v3

Do not dynamically resolve "latest resume."

---

# 16. Tailored Resume

If the candidate applies using a tailored resume:

Store:

tailored_resume_id

If they apply using an existing base resume:

tailored_resume_id = null

Do not force tailoring if the candidate chooses not to use it.

---

# 17. Role Profile

Store:

role_profile_id

This allows future analytics such as:

Which role profile gets the most interviews?

Example:

FDE
Full Stack
Frontend

---

# 18. Application Preparation API

Add:

POST

/api/v1/jobs/{job_id}/applications/prepare

Purpose:

Create or prepare a draft application.

Do not submit externally.

---

# 19. Preparation Response

Return:

- job
- company
- selected resume
- tailored resume
- role profile
- application URL
- missing information
- readiness status

Example:

{
  "status": "ready",
  "job_id": "...",
  "resume_id": "...",
  "tailored_resume_id": "...",
  "application_url": "...",
  "missing_items": []
}

---

# 20. Application Draft

The draft should be editable.

Example:

Application Draft

Company:
ABC Technologies

Role:
Forward Deployed Engineer

Resume:
FDE Resume v3

Tailored Resume:
Tailored Resume #17

Application URL:
Company Careers

Notes:
Interested because of implementation-focused role.

Status:
READY

---

# 21. Candidate Approval

Before an application becomes:

APPLIED

require explicit candidate action.

Example:

[Review Application]

↓

[Confirm Applied]

This prevents accidental applications.

---

# 22. Mark Applied

Add:

POST

/api/v1/applications/{application_id}/mark-applied

Request may include:

applied_at
notes

The server should create:

APPLIED

event.

---

# 23. External Submission

The initial MVP does NOT automatically submit to external sites.

The candidate may:

1. click application URL
2. apply manually
3. return to the application system
4. click "Mark as Applied"

This provides a reliable tracking workflow without violating external platform restrictions.

---

# 24. External Application URL

Store the application URL from the canonical job/source.

Do not invent URLs.

If the job has multiple source URLs:

prefer the appropriate verified application URL.

---

# 25. Duplicate Applications

Prevent accidental duplicate applications.

Recommended uniqueness rule:

candidate_id
+
job_id

should normally have one active application.

If a candidate intentionally reapplies:

allow a controlled reapplication workflow later.

Do not silently create duplicates.

---

# 26. Duplicate Detection

Before creating an application:

check:

Does candidate already have an application for this job?

If yes:

return:

existing_application

instead of silently creating another one.

---

# 27. Reapplication

If required later, support:

REAPPLICATION

with explicit candidate action.

Do not implement complex reapplication logic unless needed by current repository.

---

# 28. Application URL Validation

Validate:

- valid URL
- http/https
- safe URL handling
- no local file paths
- no javascript URLs

Do not automatically visit arbitrary URLs from application creation.

---

# 29. External Content Is Untrusted

Application URLs and job descriptions may originate from external providers.

Treat them as untrusted data.

Do not execute instructions found inside:

- job descriptions
- application pages
- source metadata

---

# 30. Application Form Data

Do not automatically store sensitive application answers without explicit need.

MVP should keep:

- application URL
- notes
- status
- resume references
- timestamps

Do not build a complete credential/application-answer vault yet.

---

# 31. Sensitive Data

Never store:

- passwords
- external platform login credentials
- OTPs
- authentication cookies
- CAPTCHA solutions

in the application record.

---

# 32. Referral Information

If the candidate applies through a referral, support:

application_method = referral

Optionally store:

referral_contact_id

only if the contact domain already exists.

Do not create a complete CRM in this phase.

---

# 33. Recruiter Contact

If a recruiter contacts the candidate, the application may record:

RECRUITER_CONTACTED

Future outreach/email domains can provide richer contact tracking.

Do not build full outreach automation here.

---

# 34. Application Notes

Candidate notes may contain:

"Applied through referral from X."

or:

"Recruiter asked me to apply through company website."

Notes belong to the candidate.

Do not expose them to other users.

---

# 35. Application Status Updates

Support:

PUT

/api/v1/applications/{application_id}

for controlled fields.

Important:

Do not allow arbitrary status transitions without validation.

---

# 36. Status Transition Rules

Example:

DRAFT
→ READY

READY
→ APPLIED

APPLIED
→ UNDER_REVIEW
→ RECRUITER_CONTACTED
→ INTERVIEWING
→ OFFER
→ REJECTED
→ WITHDRAWN
→ CLOSED

Not every transition needs to be enforced rigidly.

However, prevent obviously invalid state corruption.

---

# 37. Candidate Ownership

Every application API must derive:

candidate_id

from authenticated Firebase identity.

Never trust:

candidate_id

from request body.

---

# 38. Application Retrieval

Add:

GET

/api/v1/applications

Support filters:

status
company
role
date
source

Do not implement complex analytics here.

---

# 39. Application Detail

Add:

GET

/api/v1/applications/{application_id}

Return:

- job
- company
- status
- application URL
- selected resume
- tailored resume
- role profile
- applied date
- events
- notes

---

# 40. Application Event API

Add:

POST

/api/v1/applications/{application_id}/events

The candidate may add a valid event manually.

Example:

{
  "event_type": "INTERVIEW_COMPLETED",
  "event_at": "2026-10-15T14:00:00",
  "notes": "Technical interview completed."
}

---

# 41. Event Validation

Validate:

- event type
- timestamp
- ownership
- reasonable payload
- metadata size

Do not allow arbitrary executable data.

---

# 42. Application Timeline UI

Frontend should show:

Application Timeline

04 Oct
Application created

04 Oct
Applied

08 Oct
Recruiter contacted

15 Oct
Interview scheduled

20 Oct
Rejected

---

# 43. Application Dashboard

Add a basic application tracking page.

Example:

Applications

--------------------------------
Company       Role        Status
--------------------------------
ABC           FDE         Applied
XYZ           Frontend    Interviewing
DEF           Full Stack  Rejected
--------------------------------

Filters:

- All
- Applied
- Interviewing
- Offer
- Rejected
- Withdrawn

---

# 44. Job Detail Integration

Job Detail should eventually show:

[Match]

[Selected Resume]

[Tailored Resume]

[Prepare Application]

Once prepared:

[Review Application]

After candidate applies externally:

[Mark as Applied]

---

# 45. Application Readiness

Implement a readiness checker.

Example:

READY when:

- job exists
- application URL exists
- resume exists
- selected resume is valid
- candidate owns all related entities
- tailored resume is valid if selected
- no blocking validation errors

Otherwise:

NOT_READY

with reasons.

---

# 46. Example Not Ready

Job:

Forward Deployed Engineer

Selected resume:

FDE Resume v3

Tailored resume:

STALE

Response:

NOT_READY

Reason:

"Tailored resume is stale because the candidate profile changed."

The system should suggest:

Regenerate Tailored Resume

It must not silently regenerate it.

---

# 47. No Tailored Resume

If candidate chooses to apply using base resume:

READY

with:

tailored_resume_id = null

This is valid.

Tailoring is recommended, not mandatory.

---

# 48. Application Confirmation

Confirmation UI:

┌───────────────────────────────┐
│ Review Application             │
│                               │
│ Company: ABC                  │
│ Role: FDE                     │
│ Resume: FDE Resume v3         │
│ Tailored: Yes                 │
│                               │
│ Application URL               │
│                               │
│ [Open Application]            │
│                               │
│ After submitting:             │
│ [Mark as Applied]             │
└───────────────────────────────┘

---

# 49. No Automatic Browser Submission

Do NOT build browser automation in this phase.

Do not:

- log into LinkedIn
- log into Naukri
- submit forms automatically
- bypass CAPTCHA
- scrape authenticated pages
- simulate user interaction to evade restrictions

Provider integrations can be introduced later only where officially/permitted.

---

# 50. Future Integration Boundary

Architecture should allow:

ApplicationProvider

Possible future implementations:

- ManualApplicationProvider
- OfficialCompanyApplicationProvider
- PermittedJobBoardProvider
- UserProvidedApplicationProvider

The application service should not depend directly on a particular job board.

---

# 51. Provider Interface

If useful, define:

ApplicationProvider

with conceptual methods:

prepare_application()
submit_application()
get_application_status()

For this phase:

prepare_application()

may be implemented.

submit_application()

should remain unavailable/unimplemented for unrestricted external sites.

---

# 52. Why Provider Abstraction?

Because:

LinkedIn
Naukri
Indeed
Wellfound
Company Careers

all have different:

- workflows
- APIs
- permissions
- authentication
- application forms
- policies

Do not hard-code application logic into the core domain.

---

# 53. No Credential Storage

Provider credentials belong in secure integration infrastructure later.

Never store:

username/password

inside:

applications

---

# 54. Application Source

Preserve provenance.

Example:

Job source:

company career page

Application source:

company career page

Another:

Job discovered through:

LinkedIn

Application submitted manually through:

Company Careers

These are not necessarily the same.

Therefore keep:

job source

and:

application source

separate.

---

# 55. Application Events and External Status

Later integrations may automatically produce:

RECRUITER_CONTACTED
INTERVIEW_SCHEDULED
REJECTED

For MVP, these are manually recorded.

---

# 56. Email Integration Boundary

Do not implement email tracking fully in this phase.

Later:

Email
↓
Application matching
↓
Application Event

This belongs to a later email/integration phase.

---

# 57. Analytics Preparation

Store enough information for future analysis:

- application date
- company
- role
- source
- resume used
- role profile used
- job location
- match category
- tailored resume
- result
- status changes
- events

Later analytics can answer:

Which role gets the most interviews?

Which source produces the best response rate?

Which resume performs best?

Which companies respond?

Which skills correlate with interviews?

Do not build those analytics now.

---

# 58. Application Funnel

The data should support:

Jobs Discovered
        ↓
Jobs Matched
        ↓
Resume Selected
        ↓
Resume Tailored
        ↓
Applications Prepared
        ↓
Applications Submitted
        ↓
Recruiter Contact
        ↓
Interview
        ↓
Offer
        ↓
Accepted / Rejected

---

# 59. Conversion Metrics Later

Do not implement analytics yet.

But preserve data required for:

match → application
application → response
response → interview
interview → offer

This will become one of the strongest product feedback loops.

---

# 60. Application API Summary

Implement:

POST
/api/v1/jobs/{job_id}/applications/prepare

GET
/api/v1/applications

GET
/api/v1/applications/{application_id}

PUT
/api/v1/applications/{application_id}

POST
/api/v1/applications/{application_id}/mark-applied

POST
/api/v1/applications/{application_id}/events

---

# 61. Optional Delete/Archive

Prefer:

archive/close

over destructive deletion when application history exists.

Historical application records are valuable.

If deletion is required by privacy functionality, ensure related derived data is handled correctly.

---

# 62. Frontend Services

Add/reuse:

application.service.ts

Responsibilities:

- prepare
- list
- get
- update
- mark applied
- add event

Do not put business logic inside Angular components.

---

# 63. Frontend Pages

Implement:

1. Application preparation/review
2. Application list
3. Application detail/timeline

Keep UI simple.

Do not build an elaborate CRM dashboard yet.

---

# 64. Testing

Unit tests:

- application creation
- duplicate detection
- readiness validation
- status transitions
- event creation
- ownership
- historical resume references
- stale tailored resume
- missing resume
- missing application URL

---

# 65. Integration Tests

Test:

Job
→ Resume Selection
→ Tailored Resume
→ Application Preparation

Expected:

application draft created correctly.

Then:

mark applied

Expected:

status = APPLIED

and:

APPLIED event created.

---

# 66. Duplicate Test

Candidate already applied to:

Job A

Candidate attempts:

prepare application for Job A

Expected:

existing application returned.

No duplicate active application.

---

# 67. Historical Resume Test

Application created using:

Resume v3

Candidate uploads:

Resume v4

Expected application still references:

Resume v3

---

# 68. Stale Tailored Resume Test

Application preparation uses:

Tailored Resume #1

Then candidate profile changes.

Tailored Resume #1 becomes:

STALE

Expected:

application preparation blocks use of stale tailored resume.

Candidate can either:

regenerate

or:

choose a valid base resume.

---

# 69. Ownership Test

Candidate A requests:

Candidate B application

Expected:

403/404 according to existing authorization conventions.

Do not leak existence of private records.

---

# 70. Status Test

Create:

DRAFT

Then:

READY

Then:

APPLIED

Verify events are created correctly.

---

# 71. Event Test

Add:

INTERVIEW_COMPLETED

Expected:

application timeline contains event.

---

# 72. Security

Continue Firebase Authentication.

Use existing authorization patterns.

Private application data must never be publicly accessible.

Validate all foreign keys belong to the current candidate.

---

# 73. Audit

Important actions should be auditable:

- application created
- application marked applied
- status changed
- resume selected
- tailored resume used
- application withdrawn

Reuse existing audit infrastructure if already implemented.

Do not duplicate audit systems.

---

# 74. No LLM Required

Application tracking itself should be deterministic.

Do not use Gemini to:

- create application status
- decide whether candidate applied
- invent application events
- infer interview outcomes

AI can be introduced later for useful tasks such as:

- summarizing recruiter emails
- extracting interview details
- identifying rejection reasons

but those are future capabilities.

---

# 75. Prompt Injection Boundary

No LLM is required for the core phase.

External job content must still be treated as untrusted.

Do not let application URLs or job descriptions trigger arbitrary actions.

---

# 76. Acceptance Criteria

Phase 10.20 is complete when:

- [ ] Application domain exists.
- [ ] Candidate owns applications.
- [ ] Job is linked correctly.
- [ ] Resume used is recorded.
- [ ] Resume version is recorded.
- [ ] Tailored resume is recorded when used.
- [ ] Role profile is recorded.
- [ ] Application URL is preserved.
- [ ] Application source/method is preserved.
- [ ] Application status is controlled.
- [ ] Application events are persisted.
- [ ] Application history is preserved.
- [ ] Duplicate applications are prevented.
- [ ] Application readiness is validated.
- [ ] Candidate approval is required before marking applied.
- [ ] External submission is NOT automated.
- [ ] No credentials are stored.
- [ ] No CAPTCHA bypass exists.
- [ ] No unrestricted browser automation exists.
- [ ] Application timeline exists.
- [ ] Basic application dashboard exists.
- [ ] Historical resume references remain stable.
- [ ] Stale tailored resumes are detected.
- [ ] Ownership tests pass.
- [ ] Integration tests pass.
- [ ] Existing functionality remains intact.

---

# 77. Codex Instructions

Implement Phase 10.20 only.

Before coding:

1. Read this entire specification.
2. Inspect actual Phase 10.19 implementation.
3. Inspect Phase 10.18 Resume Selection.
4. Inspect Job and Job Source models.
5. Inspect Tailored Resume models.
6. Inspect Resume models.
7. Inspect Role Profile models.
8. Inspect existing authentication/authorization.
9. Inspect audit infrastructure.
10. Inspect frontend job detail.
11. Inspect existing migrations.
12. Inspect existing API conventions.

The current repository is authoritative.

Do not assume the documentation exactly matches implementation.

Reuse existing infrastructure.

---

# 78. Architecture Rules

Continue using:

Angular
FastAPI
Python
PostgreSQL
SQLAlchemy
Alembic
Firebase Authentication
private object storage

Use the existing modular monolith.

Do not introduce microservices.

Do not redesign the architecture.

---

# 79. Provider Boundary

Keep future external application automation behind:

ApplicationProvider

Do not implement unrestricted external submission.

MVP submission flow is:

Candidate opens application URL
        ↓
Candidate applies manually
        ↓
Candidate returns
        ↓
Candidate clicks "Mark as Applied"
        ↓
Application becomes APPLIED

---

# 80. Do Not Implement Future Phases

Do NOT implement:

- mass auto-apply
- unrestricted browser automation
- email tracking
- recruiter outreach automation
- interview automation
- application analytics
- learning/recommendation engine
- autonomous career agent

Those are future phases.

---

# 81. Implementation Order

1. Inspect current application-related models
2. Reconcile schema with existing implementation
3. Create application migration
4. Create application-event migration
5. Create schemas
6. Create repositories
7. Create ApplicationService
8. Implement readiness checker
9. Implement duplicate detection
10. Implement application preparation
11. Implement mark-applied workflow
12. Implement event tracking
13. Implement application list/detail APIs
14. Implement frontend preparation UI
15. Implement application dashboard
16. Implement timeline
17. Add tests
18. Run migrations
19. Run backend tests
20. Run frontend tests/build
21. Verify historical references
22. Inspect/fix issues
23. Verify architecture

---

# 82. Required Final Codex Report

Report:

## Implemented

What was actually built.

## Database

List tables created/modified.

## Application Lifecycle

Explain:

DRAFT
→ READY
→ APPLIED
→ later statuses

## Resume Traceability

Explain how the exact resume used by an application is preserved.

## Application Events

Explain event storage.

## Duplicate Protection

Explain how duplicate applications are prevented.

## Security

Explain authentication and ownership.

## External Submission

Clearly state what is and is not automated.

## APIs

List all endpoints.

## Frontend

Explain pages/components.

## Tests

Give exact results.

## Warnings/Errors

List all.

## Deviations

List every deviation from this specification.

## Boundary Confirmation

Confirm:

10.19 Resume Tailoring
        ↓
10.20 Application Preparation & Tracking
        ↓
NEXT PHASE