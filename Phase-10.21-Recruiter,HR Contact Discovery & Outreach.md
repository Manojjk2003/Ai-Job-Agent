# Phase 10.21 — Recruiter / HR Contact Discovery & Outreach

## 1. Objective

Build the recruiter/contact discovery and outreach system.

The system should help answer:

- Who is an appropriate person to contact for this job?
- Is their contact information public/permitted?
- What company/job are they associated with?
- What is the best outreach channel?
- What should the candidate say?
- Has the candidate already contacted them?
- What happened afterward?

The system should support:

Contact Discovery
        ↓
Contact Validation
        ↓
Outreach Draft
        ↓
Candidate Review
        ↓
Candidate Approval
        ↓
Send
        ↓
Track Response

The system must NOT become an unrestricted messaging bot.

---

# 2. Product Principle

The goal is not:

"Find someone's private phone number."

The goal is:

"Find an appropriate, publicly available or permitted professional contact relevant to the opportunity."

Examples:

- Recruiter publicly associated with the company
- Talent acquisition professional
- Hiring manager when appropriate
- Founder/hiring contact for a small startup
- Public recruiting email
- Official company hiring email
- User-provided referral/contact

---

# 3. Privacy Boundary

Only use:

- public professional information
- information supplied by the candidate
- information obtained through permitted integrations
- official company contact information
- supported APIs/providers

Do NOT:

- discover private phone numbers
- bypass privacy controls
- scrape private profiles
- infer personal email addresses
- guess email addresses from naming patterns
- purchase leaked personal data
- use stolen databases
- circumvent access restrictions

---

# 4. Phase Boundary

Previous:

10.20 Application Preparation & Tracking

This phase adds:

10.21 Contact Discovery & Outreach

Future:

10.22 Email / Communication Tracking
10.23 Analytics / Feedback
10.24 Career Agent

Do not implement those future phases unless explicitly required by this phase.

---

# 5. Core Architecture

Use:

Candidate
    ↓
Company
    ↓
Job
    ↓
Contact
    ↓
Outreach

A contact may be associated with:

- Company
- Job
- Application
- Candidate
- Outreach

---

# 6. Contact vs Outreach

These are different concepts.

Contact:

"John is a recruiter at Company X."

Outreach:

"Manoj sent John a message regarding the FDE position."

Therefore:

Contact != Outreach

---

# 7. Contact Domain

Reuse an existing contact model if present.

If not implemented, create:

contacts

Suggested fields:

id
company_id
name
first_name
last_name
job_title
department
email
phone
profile_url
source
source_url
contact_type
status
confidence
is_public
last_verified_at
created_at
updated_at

---

# 8. Contact Type

Controlled values:

RECRUITER
TALENT_ACQUISITION
HIRING_MANAGER
HR
FOUNDER
TEAM_LEAD
EMPLOYEE_REFERRAL
GENERAL_HIRING_CONTACT
COMPANY_CONTACT
OTHER

---

# 9. Contact Source

Examples:

OFFICIAL_COMPANY_SITE
USER_PROVIDED
PUBLIC_PROFILE
PERMITTED_PROVIDER
COMPANY_JOB_POSTING
REFERRAL
OTHER

Never claim a source that was not actually used.

---

# 10. Contact Confidence

Use:

HIGH
MEDIUM
LOW
UNKNOWN

Confidence describes the reliability of the contact association.

Example:

Official company recruiting email:

HIGH

Public profile clearly showing:
"Talent Acquisition at Company X"

HIGH/MEDIUM

User-provided contact:

HIGH for ownership, but source should remain USER_PROVIDED.

---

# 11. Public Contact Indicator

Store:

is_public

This should indicate whether the information is explicitly public/permitted.

Do not assume:

"found online"

means:

"allowed to use."

Provider policies and source permissions must still be respected.

---

# 12. Contact Validation

A contact may become stale.

Store:

last_verified_at

and optionally:

verification_status

Possible values:

VERIFIED
UNVERIFIED
STALE
INVALID
UNKNOWN

---

# 13. Company Association

A contact should normally belong to a canonical company.

Example:

Company:
ABC Technologies

Contact:
Jane Doe

Role:
Talent Acquisition

Association:

Company ABC
    ↓
Jane Doe

Do not create duplicate company records.

Reuse the existing Company domain.

---

# 14. Job Association

A recruiter may be associated with a particular job.

Example:

Jane Doe
Talent Acquisition
ABC Technologies

Job:
Forward Deployed Engineer

If the job posting explicitly identifies Jane:

store the relationship.

Otherwise:

do not invent that Jane is the hiring contact.

---

# 15. Contact Job Relationship

If needed, create:

job_contacts

Suggested fields:

id
job_id
contact_id
relationship_type
confidence
source
created_at

Relationship types:

RECRUITER
HIRING_MANAGER
HIRING_TEAM
REFERRAL
GENERAL_CONTACT
OTHER

---

# 16. Application Relationship

A contact can also be associated with an application.

Example:

Application #123
    ↓
Recruiter Jane

This becomes useful when tracking:

- recruiter contact
- recruiter response
- interview scheduling

---

# 17. Contact Discovery Provider

Do not hard-code external contact discovery.

Create:

ContactDiscoveryProvider

Conceptual interface:

search_contacts()
get_contact()
normalize_contact()
verify_contact()
health_check()

---

# 18. MVP Provider

Implement:

UserProvidedContactProvider

This allows the candidate to manually enter:

- name
- role
- company
- public email
- profile URL

This gives us a working system without relying on unrestricted scraping.

---

# 19. Official Company Contact Provider

A narrow provider may later inspect permitted official company pages for:

- careers contact
- recruiting email
- hiring email

It must not crawl the entire internet.

Do not implement broad scraping.

---

# 20. Public Professional Contact

If a permitted provider supplies:

Name:
Jane Doe

Title:
Talent Acquisition Partner

Company:
ABC Technologies

Profile:
public professional profile

The system may store it.

It must preserve:

source
source_url
retrieved_at

---

# 21. No Email Guessing

Do NOT generate:

jane.doe@company.com

from:

Jane Doe

unless the address was explicitly provided by an allowed source.

Email pattern inference is not contact discovery.

---

# 22. Contact Deduplication

Avoid duplicates using conservative rules:

1. Provider external ID
2. Exact verified email
3. Normalized profile URL
4. Company + normalized name + role

Do not merge people solely because they have the same name.

---

# 23. Example

These may be different people:

Jane Doe
Recruiter

Jane Doe
Engineering Manager

Do not merge based on name alone.

---

# 24. Contact Search API

Add:

GET

/api/v1/companies/{company_id}/contacts

Optional filters:

contact_type
status
confidence

---

# 25. Add Contact

Add:

POST

/api/v1/companies/{company_id}/contacts

Used for:

- user-provided contact
- permitted discovered contact

---

# 26. Contact Detail

Add:

GET

/api/v1/contacts/{contact_id}

Return:

- company
- name
- title
- contact type
- available professional channels
- source
- verification
- associated jobs

---

# 27. Discover Contact

Add:

POST

/api/v1/jobs/{job_id}/contacts/discover

The system should search for appropriate contacts using available permitted providers.

It should return:

- contacts
- confidence
- source
- relationship to job/company

---

# 28. Discovery Result

Example:

{
  "contacts": [
    {
      "name": "Jane Doe",
      "title": "Talent Acquisition",
      "contact_type": "RECRUITER",
      "confidence": "high",
      "source": "OFFICIAL_COMPANY_SITE"
    }
  ]
}

---

# 29. No Fake Contacts

If no contact is found:

return:

NO_CONTACT_FOUND

Do not generate a hypothetical recruiter.

---

# 30. Contact Ranking

If multiple contacts exist, rank them.

Possible priority:

1. Recruiter explicitly associated with job
2. Talent acquisition associated with company
3. Hiring manager associated with job/team
4. Official recruiting contact
5. Relevant founder/hiring contact for startup
6. General company contact

Do not rank based solely on seniority.

---

# 31. Job Relevance

A contact associated with the specific job should generally rank higher.

Example:

Job:
FDE

Contact:
Recruiter for Engineering

better than:

Contact:
Recruiter for Finance

---

# 32. Contact Recommendation

The system may return:

Recommended contact:

Jane Doe
Talent Acquisition
ABC Technologies

Reason:

- Associated with engineering hiring
- Public professional contact
- Relevant to this job

---

# 33. Candidate Choice

The candidate must be able to select:

Use Jane Doe

or:

Choose another contact

Do not automatically contact the highest-ranked person.

---

# 34. Outreach Domain

Create/reuse:

outreach

Suggested fields:

id
candidate_id
contact_id
company_id
job_id
application_id
channel
subject
body
status
draft_method
approved_at
sent_at
created_at
updated_at

---

# 35. Outreach Status

Use:

DRAFT
REVIEW_REQUIRED
APPROVED
SENDING
SENT
DELIVERED
REPLIED
BOUNCED
FAILED
CANCELLED

Do not mark:

SENT

until the provider confirms the message was actually sent.

---

# 36. Outreach Channels

Support:

EMAIL
LINKEDIN
COMPANY_CONTACT_FORM
OTHER_PERMITTED_CHANNEL

MVP should primarily support:

EMAIL
USER_PROVIDED

and manual copy/share workflows for other channels.

---

# 37. No Unauthorized Messaging

Do not automatically send messages through:

- LinkedIn
- Naukri
- other social platforms

unless an official/permitted integration exists.

---

# 38. Outreach Draft

The system should generate:

Subject

and:

Body

based on:

- candidate profile
- job
- company
- role profile
- selected resume
- application status
- contact role

---

# 39. Example Outreach

Subject:

Interest in the Forward Deployed Engineer role

Body should communicate:

- candidate identity
- role of interest
- relevant truthful experience
- why the role is relevant
- concise call to action

Avoid generic spam language.

---

# 40. Personalization

Personalization should come from actual evidence.

Possible:

Company:
ABC Technologies

Job:
Forward Deployed Engineer

Candidate evidence:
requirements gathering
FastAPI
AWS
deployment

Draft can mention these.

Do not fabricate:

"I have followed ABC Technologies for years."

unless candidate supplied that fact.

---

# 41. No Fake Personalization

Bad:

"I've always admired your innovative culture."

unless candidate explicitly provided that sentiment.

The system should prefer concrete relevance.

---

# 42. Outreach Structure

A good short outreach may contain:

1. Who I am
2. Why I am contacting you
3. Specific role
4. Relevant experience
5. Simple CTA

Keep it concise.

---

# 43. Resume Attachment

Do not automatically attach files without candidate approval.

Candidate should explicitly choose:

Attach tailored resume

or:

Do not attach.

---

# 44. Resume Link

If using a link:

use a secure/private mechanism.

Do not expose private object storage URLs.

Prefer:

controlled application/download flow

if a shareable artifact is eventually required.

---

# 45. Outreach Source

Store:

draft_method

Possible:

TEMPLATE
AI
MANUAL
HYBRID

AI-generated drafts must still be reviewed.

---

# 46. AI Provider

Use existing AI provider abstraction.

Example:

OutreachGenerationProvider

Implementation:

GeminiOutreachProvider

Do not hard-code Gemini into the OutreachService.

---

# 47. AI Prompt

Prompt should explicitly state:

Use only supplied candidate facts.

Do not:

- invent experience
- invent relationship with contact
- invent familiarity with company
- invent mutual connections
- invent achievements
- claim previous communication
- claim referral
- claim employment
- claim certifications

---

# 48. Contact Data Protection

Do not ask the model to infer:

- private email
- phone number
- personal information

The model receives only the contact fields required to generate the message.

---

# 49. Structured Output

Prefer:

{
  "subject": "...",
  "body": "...",
  "personalization_points": [
    "..."
  ],
  "sources": [
    "job:...",
    "candidate_experience:..."
  ]
}

The final text should still be validated.

---

# 50. Outreach Claim Validation

Validate generated statements.

Example:

"I saw your post about hiring FDEs."

Only allowed if a source exists.

If no source:

remove/reject.

---

# 51. Human Approval

Required workflow:

Draft
↓
Review
↓
Approve
↓
Send

No direct:

Generate
↓
Send

workflow.

---

# 52. Outreach Review UI

Example:

----------------------------------------
OUTREACH DRAFT
----------------------------------------

To:
Jane Doe
Talent Acquisition

Company:
ABC Technologies

Subject:
Interest in Forward Deployed Engineer role

Body:
...

Sources:
✓ Job description
✓ Candidate profile
✓ FDE role profile

[Edit]
[Regenerate]
[Approve & Send]
[Cancel]

----------------------------------------

---

# 53. Manual Editing

Candidate must be able to edit:

- subject
- body
- recipient/channel
- attachment choice

Manual edits should not be overwritten by regeneration unless explicitly requested.

---

# 54. Approval Record

When approved, store:

approved_at
approved_by

The approved user should be the authenticated candidate.

---

# 55. Sending Boundary

The core system should use:

OutreachProvider

Interface:

prepare()
send()
get_status()
cancel()

MVP may implement:

ManualOutreachProvider

and, where a supported email integration exists:

EmailOutreachProvider

---

# 56. Email Provider

Do not build SMTP credentials into the core application.

Use a supported email integration/provider abstraction.

Provider credentials should remain outside normal application records.

---

# 57. Manual Workflow

For MVP, the candidate can:

Generate draft
↓
Copy
↓
Open email
↓
Send manually
↓
Return
↓
Mark sent

This is acceptable.

---

# 58. Send Confirmation

If using manual sending:

POST:

/api/v1/outreach/{outreach_id}/mark-sent

This records:

SENT

and:

sent_at

The candidate confirms the action.

---

# 59. Provider Send

If a permitted email integration exists:

POST:

/api/v1/outreach/{outreach_id}/send

The backend invokes the configured provider.

Never expose provider credentials to Angular.

---

# 60. Duplicate Outreach Protection

Before sending:

check whether the candidate has already contacted the same person regarding the same job.

Warn:

"An outreach message was already sent to this contact for this job."

Do not silently send duplicates.

---

# 61. Contact Frequency

Do not implement automated spam campaigns.

Later rate limits may include:

- maximum outreach/day
- maximum outreach/company
- cooldown per contact

For MVP, prevent accidental duplicate outreach.

---

# 62. Outreach Events

Create/reuse:

outreach_events

Suggested:

id
outreach_id
event_type
event_at
metadata
created_at

Events:

DRAFT_CREATED
EDITED
APPROVED
SENT
DELIVERED
REPLIED
BOUNCED
FAILED
CANCELLED

---

# 63. Outreach Timeline

Example:

04 Oct
Draft created

04 Oct
Candidate approved

04 Oct
Sent

07 Oct
Reply received

---

# 64. Response Tracking

Do not implement full email parsing in this phase.

If a response is manually recorded:

REPLIED

can be added as an event.

Automated email tracking belongs to a later phase.

---

# 65. Application Relationship

Outreach should optionally reference:

application_id

Example:

Application:
ABC FDE

Outreach:
Contacted recruiter Jane

This enables:

Application
    ↓
Outreach
    ↓
Recruiter

---

# 66. Outreach Without Application

Allow:

candidate → job → recruiter → outreach

even if the candidate has not applied yet.

This supports:

"Should I contact the recruiter before applying?"

However, clearly track:

application_id = null

---

# 67. Outreach After Application

Also support:

Application
    ↓
Recruiter Outreach

This is a common workflow.

---

# 68. Contact Discovery + Outreach Flow

Example:

User:

"Find someone I can contact about this FDE role."

System:

Job
↓
Company
↓
Contact discovery
↓
Found recruiter
↓
Show source/confidence
↓
Candidate selects contact
↓
Generate outreach draft
↓
Candidate reviews
↓
Candidate approves
↓
Send/manual send
↓
Track event

---

# 69. No Autonomous Agent Sending

The Career Agent may later orchestrate:

discover
→ recommend
→ draft

but must stop at:

REQUIRES_APPROVAL

before sending.

---

# 70. Agent Permission Boundary

Agent may:

READ:
- jobs
- companies
- candidate profile
- role profiles
- applications

CREATE:
- contact discovery run
- outreach draft

CANNOT automatically:

- send message
- change candidate profile
- apply to job
- connect external account

without explicit approval.

---

# 71. Contact Discovery Runs

If discovery providers are used, optionally create:

contact_discovery_runs

Suggested:

id
candidate_id
company_id
job_id
provider_name
status
result_count
started_at
completed_at
error_message
created_at

This follows the same discovery-run architecture used for:

Company Discovery
Hiring Source Discovery
Job Discovery

---

# 72. Provider Provenance

Every discovered contact should preserve:

provider
source
source_url
retrieved_at

This makes contact discovery auditable.

---

# 73. No Unrestricted Scraping

Do not implement generic:

"Search Google and scrape everything."

Do not build:

- LinkedIn scraper
- Naukri scraper
- private-profile scraper
- search-engine scraping system

Use permitted providers and public/official sources.

---

# 74. API Summary

Implement:

GET
/api/v1/companies/{company_id}/contacts

POST
/api/v1/companies/{company_id}/contacts

GET
/api/v1/contacts/{contact_id}

POST
/api/v1/jobs/{job_id}/contacts/discover

GET
/api/v1/jobs/{job_id}/contacts

POST
/api/v1/jobs/{job_id}/outreach

GET
/api/v1/outreach

GET
/api/v1/outreach/{outreach_id}

PUT
/api/v1/outreach/{outreach_id}

POST
/api/v1/outreach/{outreach_id}/approve

POST
/api/v1/outreach/{outreach_id}/send

POST
/api/v1/outreach/{outreach_id}/mark-sent

POST
/api/v1/outreach/{outreach_id}/events

---

# 75. Frontend

Add:

Contacts panel
Outreach composer
Outreach history

Job Detail:

----------------------------------
Job
----------------------------------

Match
Resume
Application

Recruiter / Contact
Jane Doe
Talent Acquisition

[Find Contacts]

Outreach

[Create Outreach]

----------------------------------

---

# 76. Contact Selection UI

Show:

Name
Role
Company
Relationship
Source
Confidence

Example:

Jane Doe
Talent Acquisition
ABC Technologies

Relationship:
Engineering recruiting

Source:
Official company source

Confidence:
High

[Select]

---

# 77. Outreach Composer

Fields:

To
Subject
Message
Attach Resume

Buttons:

[Generate Draft]
[Edit]
[Approve]
[Send]

---

# 78. Safety Confirmation

Before send:

"You're about to send this message to Jane Doe regarding the Forward Deployed Engineer position."

Require:

[Confirm Send]

---

# 79. Security

All contact and outreach APIs require authentication.

Candidate ownership must be enforced.

Do not expose another candidate's:

- contacts
- notes
- outreach
- communication history

---

# 80. Authorization

Contact records associated with shared companies may have a distinction between:

global company contact data

and:

candidate-specific discovery history.

Do not accidentally expose candidate-private discovery metadata to other candidates.

---

# 81. Company Contact vs Candidate Contact

Important distinction:

Company contact:

"Jane Doe is a recruiter at ABC."

Candidate-specific discovery:

"Candidate X found Jane through provider Y."

The first may be shared canonical data.

The second should be candidate-private.

---

# 82. Data Model Separation

Prefer:

contacts
    ↓
canonical contact

contact_discovery_runs
    ↓
candidate-specific discovery

outreach
    ↓
candidate-specific communication

---

# 83. Testing

Unit tests:

- contact creation
- contact normalization
- deduplication
- confidence
- contact ranking
- outreach generation
- claim validation
- approval
- duplicate outreach
- status transitions

---

# 84. Contact Security Tests

Test:

- candidate ownership
- company association
- cross-candidate discovery isolation
- invalid contact data
- malicious URLs
- private information rejection
- duplicate contacts

---

# 85. Outreach Security Tests

Test:

- unauthenticated access
- cross-candidate access
- sending without approval
- sending cancelled outreach
- duplicate send
- invalid recipient
- malicious URL
- attachment ownership

---

# 86. AI Tests

Provide a fake/mocked AI provider.

Test:

Input:

candidate:
Python, FastAPI

Job:
FastAPI Engineer

Model returns:

"10 years of FastAPI experience."

Expected:

claim rejected.

---

# 87. AI Hallucination Test

Model returns:

"I spoke with Jane last week."

No evidence.

Expected:

rejected.

---

# 88. Personalization Test

Candidate evidence:

"TPT project used FastAPI."

Job:

"Build APIs using FastAPI."

Expected outreach can mention:

FastAPI experience.

---

# 89. Unsupported Personalization Test

No evidence:

"I have followed your company for years."

Expected:

not included.

---

# 90. Duplicate Outreach Test

Existing:

Candidate
→ Jane
→ Job A
→ SENT

Candidate attempts another send.

Expected:

warning/block according to duplicate policy.

---

# 91. Approval Test

Generated outreach:

DRAFT

Attempt:

SEND

without approval.

Expected:

blocked.

After:

APPROVED

send becomes available.

---

# 92. Manual Send Test

Candidate clicks:

Mark Sent

Expected:

SENT event created.

---

# 93. Provider Failure

Email provider returns error.

Expected:

FAILED

with safe error information.

Never expose:

- provider credentials
- authentication tokens
- secrets

---

# 94. Acceptance Criteria

Phase 10.21 is complete when:

- [ ] Contact domain exists.
- [ ] Contacts can be associated with companies.
- [ ] Contacts can optionally be associated with jobs.
- [ ] Public/permitted source is recorded.
- [ ] Contact confidence is recorded.
- [ ] Contact discovery abstraction exists.
- [ ] User-provided contacts work.
- [ ] No private-data discovery exists.
- [ ] No email guessing exists.
- [ ] Contact deduplication exists.
- [ ] Relevant contacts can be ranked.
- [ ] Outreach domain exists.
- [ ] Outreach drafts can be created.
- [ ] Candidate facts are used for personalization.
- [ ] Unsupported claims are rejected.
- [ ] Candidate approval is required before sending.
- [ ] Manual send workflow exists.
- [ ] Permitted email provider can be plugged in.
- [ ] Duplicate outreach is prevented/warned.
- [ ] Outreach events are stored.
- [ ] Application relationship is supported.
- [ ] Private data is protected.
- [ ] No unrestricted LinkedIn/Naukri automation exists.
- [ ] No private profile scraping exists.
- [ ] No mass messaging exists.
- [ ] Tests pass.
- [ ] Existing functionality remains intact.

---

# 95. Codex Instructions

Implement Phase 10.21 only.

Before coding:

1. Read this entire specification.
2. Inspect actual Phase 10.20 implementation.
3. Inspect Company models.
4. Inspect Job models.
5. Inspect Application models.
6. Inspect existing discovery provider abstractions.
7. Inspect Hiring Source providers.
8. Inspect authentication/authorization.
9. Inspect storage.
10. Inspect Gemini/provider abstraction.
11. Inspect audit infrastructure.
12. Inspect frontend Job Detail.
13. Inspect current migration structure.

The current repository is authoritative.

Reuse existing patterns.

Do not duplicate provider abstractions if an existing generic provider boundary can be extended safely.

---

# 96. Architecture Rules

Continue using:

Angular
FastAPI
Python
PostgreSQL
SQLAlchemy
Alembic
Firebase Authentication
Gemini through provider abstraction
private storage

Continue the modular-monolith architecture.

Do not introduce microservices.

---

# 97. Important Provider Rule

Provider implementations must not become business logic.

Architecture:

API
 ↓
Outreach/Contact Service
 ↓
Provider Interface
 ↓
Provider Implementation

Not:

Angular
 ↓
LinkedIn/Naukri/etc.

---

# 98. Do Not Implement Future Phases

Do NOT implement:

- unrestricted auto-apply
- mass outreach
- browser automation
- CAPTCHA bypass
- email inbox synchronization
- automatic recruiter response interpretation
- interview scheduling
- application analytics
- autonomous career agent

Those belong to future phases.

---

# 99. Implementation Order

1. Inspect existing models/provider architecture
2. Reconcile Contact domain
3. Create contact migration
4. Create contact-job relationships if required
5. Create discovery-run model if required
6. Create Outreach domain
7. Create outreach-event model
8. Create schemas
9. Create repositories
10. Implement ContactService
11. Implement ContactDiscoveryProvider boundary
12. Implement UserProvidedContactProvider
13. Implement contact ranking
14. Implement OutreachService
15. Implement AI draft provider
16. Implement claim validation
17. Implement approval workflow
18. Implement manual-send workflow
19. Implement provider send boundary
20. Implement APIs
21. Implement frontend contact UI
22. Implement outreach composer
23. Implement outreach history
24. Add tests
25. Run migrations
26. Run backend tests
27. Run frontend tests/build
28. Inspect generated outreach
29. Fix issues
30. Verify security/architecture

---

# 100. Required Final Codex Report

Report:

## Implemented

Everything actually built.

## Database

List:

- contacts
- job_contacts
- contact_discovery_runs
- outreach
- outreach_events

or the actual names used.

## Contact Discovery

Explain:

- providers
- sources
- ranking
- confidence
- deduplication

## Outreach

Explain:

- draft generation
- personalization
- claim validation
- approval
- sending
- tracking

## AI

Explain:

- provider
- prompt
- structured output
- validation
- hallucination prevention

## Security

Explain:

- ownership
- public/private data
- credential handling
- provider isolation

## APIs

List all endpoints.

## Frontend

Explain:

- contact UI
- outreach composer
- history

## Tests

Give exact results.

## Warnings/Errors

List all.

## Deviations

List every deviation from this specification.

## External Automation

Clearly state:

- what is automated
- what requires candidate approval
- what is intentionally not implemented

## Boundary Confirmation

Confirm:

10.20 Application Preparation & Tracking
        ↓
10.21 Contact Discovery & Outreach
        ↓
NEXT: 10.22 Communication / Email Tracking