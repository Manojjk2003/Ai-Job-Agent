# Phase 10.14 — Job Discovery

## 1. Purpose

Phase 10.14 introduces the system's first actual job-opening discovery capability.

The previous phases established:

    Candidate
        ↓
    Preferences
        ↓
    Preferred Location
        ↓
    Companies
        ↓
    Hiring Sources

Phase 10.14 now answers:

> What current job openings can we discover from those companies and hiring sources?

The flow becomes:

    Company
        ↓
    Hiring Sources
        ↓
    Job Discovery
        ↓
    Raw Job Results
        ↓
    Normalize
        ↓
    Deduplicate
        ↓
    Canonical Job
        ↓
    Store in PostgreSQL

This phase does NOT perform candidate-job matching yet.

Matching is Phase 10.17.

---

# 2. Product Principle

The product should not be:

    Search every job board
        ↓
    Dump thousands of jobs
        ↓
    Ask AI to rank them

Instead:

    Candidate preferences
            ↓
    Relevant companies
            ↓
    Company-specific hiring sources
            ↓
    Current openings
            ↓
    Canonical jobs
            ↓
    Later: candidate matching

This preserves the product's company-first differentiation.

---

# 3. Important Distinction

Phase 10.12:

    "Which companies are relevant?"

Phase 10.13:

    "Where does each company hire?"

Phase 10.14:

    "What jobs are currently available?"

Phase 10.16:

    "What does each JD require?"

Phase 10.17:

    "How well does the candidate match?"

Do not combine these phases.

---

# 4. Scope

Phase 10.14 includes:

- Job model
- Job location model
- Job source model
- Canonical job records
- Job discovery provider abstraction
- Source-specific job discovery
- User-provided job discovery
- Job normalization
- Job deduplication
- Job freshness/status
- Job-source relationships
- Company-job relationship
- Location-aware job discovery
- Search/discovery APIs
- Frontend job discovery UI
- Tests
- PostgreSQL persistence

---

# 5. Explicitly NOT Included

Do NOT implement:

- JD analysis
- Candidate-job matching
- ATS scoring
- Resume selection
- Resume tailoring
- Applications
- Outreach
- Email tracking
- RAG
- Qdrant indexing
- Gemini reasoning
- Agent orchestration
- Auto-apply
- Browser automation
- Unrestricted scraping

These belong to later phases.

---

# 6. Canonical Job

A job may appear on multiple sources.

Example:

    Frontend Engineer
    Acme Technologies
    Bangalore

may appear on:

    Acme Careers
    LinkedIn
    Indeed

These must not become three unrelated jobs.

Instead:

    Canonical Job
          |
          +---- Job Source A
          +---- Job Source B
          +---- Job Source C

This is one of the most important data-model decisions in this phase.

---

# 7. Job Tables

Create:

    jobs

and:

    job_sources

Optionally:

    job_locations

depending on the existing schema design.

The approved global architecture already expects:

    job
    job_source
    job_location
    job_skill
    job_requirement

Phase 10.14 should establish the foundational job/job-source/job-location domain.

Do not implement skill extraction or requirements analysis yet.

---

# 8. Jobs Table

Recommended fields:

    id
    company_id
    canonical_title
    normalized_title
    description
    employment_type
    seniority
    workplace_mode
    department
    experience_min
    experience_max
    salary_min
    salary_max
    salary_currency
    salary_period
    application_url
    status
    first_seen_at
    last_seen_at
    last_verified_at
    created_at
    updated_at

Some fields may remain NULL.

Do not invent values.

---

# 9. Why Company ID Is Required

Every discovered job should ideally be associated with a canonical company.

Example:

    jobs.company_id
        ↓
    companies.id

This lets the system answer:

    "Show me jobs from companies around HSR Layout."

It also allows company-level hiring intelligence later.

---

# 10. Job Title

Store:

    canonical_title

and:

    normalized_title

Example:

    canonical_title:
    Senior Frontend Engineer

    normalized_title:
    senior frontend engineer

The canonical title is display-facing.

The normalized title is used for search and deduplication.

---

# 11. Do Not Over-Normalize Titles

Do not automatically transform:

    Senior Frontend Engineer

into:

    Software Engineer

unless there is a later controlled title taxonomy.

Job title normalization should remain conservative.

Different titles may represent genuinely different jobs.

---

# 12. Job Description

Store the source-provided description.

This is untrusted external content.

Do not modify the original content during normalization.

If later AI analysis is performed, it should operate on the stored source data.

---

# 13. Preserve Original Job Data

The canonical job should preserve normalized information.

But source-specific records should retain enough information to trace the original listing.

This is important for:

- debugging
- source verification
- duplicate detection
- freshness
- future provider improvements

---

# 14. Job Source

Create:

    job_sources

Recommended fields:

    id
    job_id
    company_hiring_source_id
    external_job_id
    source_url
    normalized_source_url
    source_title
    source_description
    source_metadata
    status
    first_seen_at
    last_seen_at
    last_verified_at
    created_at
    updated_at

`source_metadata` may use JSONB where appropriate.

Do not store provider credentials here.

---

# 15. Why Job Sources Need Their Own Table

Example:

    Job:
    Frontend Engineer

    Sources:
        Company Careers
        LinkedIn
        Indeed

Each source may have:

- different URL
- different external ID
- different title formatting
- different description formatting
- different timestamps

The canonical job represents the job.

The source record represents the listing.

---

# 16. Job Location

A job may have multiple locations.

Example:

    Bangalore
    Pune
    Mumbai

Create:

    job_locations

Recommended:

    id
    job_id
    location_name
    area
    city
    state
    country
    postal_code
    latitude
    longitude
    location_type
    is_primary
    created_at
    updated_at

Do not implement geographic calculations yet.

---

# 17. Remote / Hybrid / Onsite

Use:

    workplace_mode

Possible values:

    remote
    hybrid
    onsite
    flexible
    unknown

Do not use a separate:

    is_remote

boolean.

A job may be:

    hybrid

which is not equivalent to:

    remote = false

---

# 18. Employment Type

Controlled values may include:

    full_time
    part_time
    contract
    internship
    freelance
    temporary
    unknown

Do not infer employment type if the source does not provide evidence.

---

# 19. Seniority

Possible values:

    intern
    junior
    mid
    senior
    lead
    manager
    director
    unknown

Do not use AI to determine seniority in Phase 10.14.

If a source explicitly provides it, normalize it.

Otherwise:

    unknown

---

# 20. Salary

Salary fields are optional:

    salary_min
    salary_max
    salary_currency
    salary_period

Example:

    700000
    1000000
    INR
    yearly

Do not convert currencies in this phase.

Do not invent salary values.

If the job says:

    Competitive salary

store:

    NULL

rather than guessing.

---

# 21. Experience

Optional fields:

    experience_min
    experience_max

Example:

    1
    3

If the source says:

    2+ years

store:

    experience_min = 2
    experience_max = NULL

Do not interpret vague wording into exact numbers.

---

# 22. Application URL

Store:

    application_url

This is where the candidate may eventually apply.

However:

Phase 10.14 does NOT submit applications.

It only discovers and stores the URL.

---

# 23. Job Status

Use controlled values:

    active
    inactive
    expired
    unknown

A discovered job should not automatically remain active forever.

---

# 24. Important Status Rule

If a job disappears from a source:

Do NOT immediately delete it.

Instead:

    mark inactive/expired

This preserves historical application and analytics data later.

---

# 25. Job Freshness

Track:

    first_seen_at
    last_seen_at
    last_verified_at

Example:

    first_seen:
    October 1

    last_seen:
    October 4

This lets the system reason about freshness later.

---

# 26. Current Job vs Historical Job

A job can become inactive.

Example:

    Oct 1:
    active

    Oct 10:
    no longer found

The canonical job remains in PostgreSQL.

Status becomes:

    inactive

This is important because later an application may refer to the historical job.

---

# 27. Job Discovery Provider

Create:

    JobDiscoveryProvider

Conceptually:

    search_jobs()
    get_job()
    normalize_job()
    health_check()

Use the existing provider architecture.

Do not create another unrelated integration system.

---

# 28. Provider Responsibility

A job provider should answer:

> What job listings can this source provide?

It should NOT:

- match candidates
- generate resumes
- send applications
- contact recruiters
- make hiring decisions

Provider = data acquisition boundary.

---

# 29. Provider Inputs

A provider may receive:

    company
    hiring source
    location
    keywords
    role context
    pagination
    maximum results

Example:

    Company:
    Acme Technologies

    Hiring source:
    Official Careers

    Location:
    Bangalore

    Keywords:
    frontend

---

# 30. Source-Specific Discovery

The system should discover jobs from the company's known hiring sources.

Example:

    Acme
       ↓
    Official Careers
       ↓
    Job Provider
       ↓
    Jobs

Then:

    Acme
       ↓
    LinkedIn
       ↓
    Job Provider
       ↓
    Jobs

The provider architecture remains source-independent.

---

# 31. User-Provided Job Provider

For MVP, implement:

    UserProvidedJobProvider

This allows manual job input.

Example:

    Company:
    Acme Technologies

    Title:
    Frontend Engineer

    URL:
    https://acme.com/careers/frontend-engineer

    Location:
    Bangalore

This lets us test the entire job domain without depending on paid APIs.

---

# 32. Why Manual Job Input Matters

We can test:

    Company
       ↓
    Hiring Source
       ↓
    Job
       ↓
    JD Analysis
       ↓
    Candidate Matching
       ↓
    Resume Tailoring

without waiting for every external provider integration.

This is important for the MVP.

---

# 33. Future Providers

Future implementations may include:

    CompanyCareerJobProvider
    PermittedJobAPIProvider
    UserProvidedJobProvider
    LinkedInProvider
    NaukriProvider
    IndeedProvider
    WellfoundProvider

Only implement providers that can be accessed legitimately.

Do not design the core application around unrestricted scraping.

---

# 34. No Scraping-First Architecture

Do NOT build:

    scrape every job board
       ↓
    dump everything into DB

Instead:

    Hiring Source
         ↓
    appropriate provider
         ↓
    normalized jobs
         ↓
    canonical job

Provider-specific access belongs behind the provider boundary.

---

# 35. Job Normalization

Raw source data:

    {
        "title": "Frontend Developer - Bangalore",
        "location": "Bengaluru",
        "employment": "Full Time",
        ...
    }

Normalized job:

    {
        "title": "Frontend Developer",
        "city": "Bangalore",
        "employment_type": "full_time"
    }

Normalization should be deterministic where possible.

---

# 36. Preserve Source Title

Do not throw away:

    source_title

Example:

    canonical_title:
    Frontend Developer

    source_title:
    Frontend Developer - Bangalore | Acme

The source value remains useful for debugging and traceability.

---

# 37. Location Normalization

Examples:

    Bengaluru
    Bangalore

may normalize to:

    Bangalore

when the mapping is known.

Similarly:

    HSR
    HSR Layout

may require contextual handling.

Do not create a complete geographic intelligence system in this phase.

---

# 38. Job Deduplication

This is one of the most important requirements.

The same job can appear on multiple sources.

Example:

    Company:
    Acme

    Title:
    Frontend Engineer

    Location:
    Bangalore

Source A:

    LinkedIn URL

Source B:

    Acme Careers URL

Source C:

    Indeed URL

These should ideally map to one:

    Canonical Job

---

# 39. Deduplication Priority

Use strong identifiers first.

Recommended order:

1. Company + provider external job ID
2. Company + normalized source URL
3. Company + application URL
4. Company + normalized title + normalized location
5. Description similarity as a later signal

Do not rely on title alone.

---

# 40. External Job ID

If a provider supplies:

    external_job_id

store it.

Example:

    linkedin:
    123456789

This is useful for repeated synchronization.

Use:

    provider + external_job_id

as an identity boundary.

---

# 41. Source URL Deduplication

If the same exact application URL appears repeatedly:

    https://acme.com/jobs/123

it should normally map to the same job.

Normalize URL carefully.

Do not blindly remove all query parameters.

---

# 42. Title + Location Deduplication

If no external ID exists:

    company
    +
    normalized title
    +
    normalized location

can be a useful candidate duplicate signal.

But this is not sufficient proof in every situation.

---

# 43. Description Similarity

Do not implement semantic job deduplication with Qdrant yet.

For MVP, description similarity can remain:

    future enhancement

If simple text hashing is useful, use it conservatively.

Do not automatically merge two jobs only because descriptions are similar.

---

# 44. Duplicate Resolution

When two listings are likely the same job:

    Canonical Job
         |
         +-- Source A
         +-- Source B

Keep both source records.

Do not delete one source listing.

---

# 45. Conflicting Job Data

Example:

    LinkedIn:
    Salary = 8-12 LPA

    Company Careers:
    Salary = not listed

Do not overwrite the source data.

Canonical fields should be derived conservatively.

Source-specific values remain available.

---

# 46. Source Priority

Future logic may prefer:

    official company source
        >
    verified provider
        >
    third-party aggregator

But do not build a complicated ranking system yet.

For MVP, preserve source provenance.

---

# 47. Company Relationship

Every canonical job should ideally have:

    company_id

If a provider cannot confidently identify the company:

    do not attach it automatically

unless the user explicitly provides the relationship.

Avoid incorrect company associations.

---

# 48. Location Relationship

A job may have:

    HSR Layout
    Bangalore

or:

    Bangalore
    Karnataka

or:

    Remote - India

Store what the source provides.

Do not invent an office location from the company's headquarters.

A company's location and a job's location are separate.

---

# 49. Remote Job

Example:

    Company:
    Bangalore

Job:

    Remote - India

Do not change the job location to:

    Bangalore

just because the company is headquartered there.

This distinction is critical for later matching.

---

# 50. Job Search Request

Recommended:

    POST /api/v1/jobs/discover

Request may include:

    company_id
    hiring_source_id
    location
    keywords
    role_profile_id
    max_results

Example:

    {
        "company_id": "...",
        "location": {
            "city": "Bangalore"
        },
        "keywords": [
            "frontend"
        ]
    }

The exact contract should follow existing API conventions.

---

# 51. Preference-Based Discovery

If the request does not specify a location:

    Candidate Preferences
         ↓
    Preferred Locations
         ↓
    Job Discovery

This enables the future assistant to handle:

    "Find jobs for me."

without asking the candidate to repeat all preferences.

---

# 52. Role Profile

A role profile may provide:

    target designation
    preferred skills
    positioning

For example:

    Frontend Engineer

It can be used as a discovery query.

But:

    discovery ≠ matching

Do not calculate candidate fit in this phase.

---

# 53. Example

Role profile:

    Full Stack Engineer

Discovery query:

    "Full Stack Engineer"

Possible results:

    Full Stack Developer
    Full Stack Engineer
    Software Engineer - Full Stack

All can be returned.

Phase 10.17 will determine candidate fit.

---

# 54. Job Discovery Service

Create:

    backend/app/services/job_discovery_service.py

Responsibilities:

- Validate request
- Resolve candidate
- Resolve company/source
- Select provider
- Discover jobs
- Normalize results
- Deduplicate
- Upsert canonical jobs
- Upsert job sources
- Upsert locations
- Update freshness
- Return results

It must NOT:

- analyze JD
- match candidate
- generate resume
- apply

---

# 55. Job Repository

Create:

    backend/app/repositories/job_repository.py

Responsibilities:

- find job
- create job
- update job
- search jobs
- find by external ID
- find by source URL
- find possible duplicates
- create/update job source
- create/update job locations

---

# 56. Schemas

Recommended:

    JobResponse
    JobLocationResponse
    JobSourceResponse
    JobDiscoveryRequest
    JobDiscoveryResponse

Keep provider-specific models internal.

---

# 57. Job APIs

Recommended:

    GET /api/v1/jobs

    GET /api/v1/jobs/{job_id}

    POST /api/v1/jobs/discover

    POST /api/v1/jobs

    GET /api/v1/jobs/{job_id}/sources

    GET /api/v1/jobs/{job_id}/locations

The exact routes must follow existing project conventions.

---

# 58. Manual Job Creation

Allow:

    POST /api/v1/jobs

for MVP/manual testing if appropriate.

Request:

    {
        "company_id": "...",
        "title": "Frontend Engineer",
        "description": "...",
        "application_url": "...",
        "employment_type": "full_time",
        "workplace_mode": "hybrid"
    }

This must not be interpreted as an application.

---

# 59. Frontend Job Discovery

Create a job discovery page.

Example:

    Job Discovery

    Location:
    [ Bangalore ]

    Role:
    [ Frontend Engineer ]

    Company:
    [ Acme Technologies ]

    [ Discover Jobs ]

    --------------------------------

    Frontend Engineer
    Acme Technologies
    Bangalore
    Hybrid
    Full Time

    [View Job]

---

# 60. Job Card

Display:

    Job Title
    Company
    Location
    Workplace Mode
    Employment Type
    Experience
    Salary if known
    Source
    Last Verified

Do not display a match score yet.

---

# 61. No Match Score

Do NOT show:

    92% match

during Phase 10.14.

Matching belongs to Phase 10.17.

The job discovery page should answer:

    "What jobs exist?"

not:

    "Should I apply?"

---

# 62. Job Detail

Display:

    Title
    Company
    Locations
    Employment Type
    Workplace Mode
    Experience
    Salary
    Description
    Application URL
    Sources
    Last Verified

Later phases can add:

    Candidate Fit
    Missing Skills
    Resume Recommendation
    Tailored Resume

---

# 63. Source Display

Example:

    Sources

    Official Careers
    Verified
    [Open Source]

    LinkedIn
    Discovered
    [Open Source]

This makes provenance visible.

---

# 64. External URL

The system should provide the original application/source URL.

The user can inspect it before applying.

Do not automatically submit anything.

---

# 65. Job Freshness

A job discovered today:

    last_seen_at = today

A job not seen for a long period can later be marked:

    inactive

Do not delete it immediately.

---

# 66. Expiration

If a provider explicitly says:

    expired

store:

    status = expired

If a provider simply stops returning it:

    do not immediately mark expired

Use a future freshness policy.

---

# 67. Discovery Run

The architecture already has search/discovery-run concepts.

Reuse the existing run infrastructure where possible.

A job discovery run may record:

    candidate
    company
    source
    query
    timestamp
    provider
    status
    result_count

Do not create multiple competing run systems.

---

# 68. Partial Results

Example:

    Company Careers → success
    LinkedIn provider → unavailable
    Indeed provider → success

Return:

    status = partial

and preserve successful jobs.

---

# 69. Provider Failure

If all providers fail:

    status = failed

with a useful error.

Do not return fake jobs.

---

# 70. Provider Timeout

External provider calls must have bounded timeouts.

Use the existing HTTP configuration.

Do not allow external sources to block FastAPI indefinitely.

---

# 71. Pagination

Providers may return many jobs.

Implement a controlled:

    max_results

and provider pagination boundary.

Do not import thousands of jobs into the MVP database by default.

---

# 72. Rate Limits

Respect provider limits.

Do not implement aggressive retries.

Future integrations must respect:

- provider API limits
- terms of service
- authentication requirements
- access restrictions

---

# 73. Search Filtering

Basic structured filters may include:

    company
    city
    area
    employment_type
    workplace_mode
    seniority
    status

Do not implement sophisticated candidate matching filters yet.

---

# 74. Job Search API

`GET /api/v1/jobs`

may support:

    search
    company_id
    city
    area
    workplace_mode
    employment_type
    status
    limit
    offset

Example:

    GET /api/v1/jobs?city=Bangalore&workplace_mode=hybrid

---

# 75. No Hardcoded Role Categories

Do not make:

    frontend
    backend
    fullstack
    FDE

hardcoded database enums for jobs.

Job titles are dynamic.

Later skill/title intelligence can classify them.

The discovery system should preserve the source title.

---

# 76. FDE Jobs

The system must support jobs such as:

    Forward Deployed Engineer
    Solutions Engineer
    Implementation Engineer
    Customer Engineer
    Field Engineer

without requiring the title to contain:

    Software Engineer

This is important for the product's broader career-role model.

---

# 77. Non-IT Future Support

The job model must not assume every job is software engineering.

Examples later:

    Data Analyst
    Product Manager
    Accountant
    Teacher
    Marketing Specialist

The canonical job entity should remain domain-neutral.

---

# 78. Job Data Quality

Required minimum identity:

    company
    title
    source/application URL

If these are missing:

    reject or mark incomplete

Do not create meaningless job records.

---

# 79. Untrusted Job Descriptions

Job descriptions can contain:

- arbitrary HTML
- scripts
- prompt injection text
- misleading instructions
- malicious URLs

Store safely.

Sanitize rendered HTML.

Do not execute scripts from job descriptions.

---

# 80. Security

Use:

- Firebase authentication
- backend authorization
- input validation
- safe URL handling
- provider credential isolation
- rate limiting where appropriate
- audit logging
- secure storage

Do not trust:

    company_id
    candidate_id
    provider_id

from the browser without validation.

---

# 81. Candidate ID

Never accept:

    candidate_id

as authoritative ownership information from the frontend.

Resolve the authenticated candidate from:

    verified Firebase UID
        ↓
    candidates.firebase_uid
        ↓
    candidate.id

This follows the existing architecture.

---

# 82. Shared Job Data

Canonical companies/jobs may eventually be shared across candidates.

Do not create duplicate jobs for each candidate.

Correct:

    Candidate A
         |
         +---- Job 123

    Candidate B
         |
         +---- Job 123

Later applications/matches will be candidate-specific.

---

# 83. Job Match Comes Later

The relationship:

    Candidate ↔ Job

will later be represented by:

    job_match

Phase 10.14 must not create match scores.

---

# 84. Application Comes Later

The relationship:

    Candidate → Job

becomes an application only after the candidate chooses to apply.

Phase 10.14 does not create:

    application

records.

---

# 85. No Resume Selection

Do not connect:

    Job
       ↓
    Resume

yet.

Resume selection is Phase 10.18.

---

# 86. No Resume Tailoring

Do not generate:

    tailored resume

from a job during Phase 10.14.

That belongs to Phase 10.19.

---

# 87. No JD Analysis

Phase 10.14 stores the raw job description.

Phase 10.16 will later analyze:

    required skills
    preferred skills
    experience
    education
    responsibilities
    eligibility
    role signals

Do not duplicate that logic here.

---

# 88. Data Flow

Complete Phase 10.14:

    Company
       ↓
    Hiring Sources
       ↓
    JobDiscoveryService
       ↓
    Provider
       ↓
    Raw Jobs
       ↓
    Normalize
       ↓
    Deduplicate
       ↓
    Canonical Jobs
       ↓
    Job Sources
       ↓
    Job Locations
       ↓
    PostgreSQL
       ↓
    Job Discovery UI

---

# 89. Backend Structure

Possible structure:

    backend/app/
    ├── api/
    │   └── v1/
    │       └── jobs.py
    │
    ├── providers/
    │   └── jobs/
    │       ├── __init__.py
    │       ├── base.py
    │       └── user_provided.py
    │
    ├── repositories/
    │   └── job_repository.py
    │
    ├── schemas/
    │   └── job.py
    │
    └── services/
        └── job_discovery_service.py

Follow existing conventions.

---

# 90. Database Relationships

Core:

    Company
       |
       +---- Jobs
               |
               +---- Job Sources
               |
               +---- Job Locations

Later:

    Job
       |
       +---- Job Requirements
       +---- Job Skills
       |
       ↓
    Candidate Match

Do not create later-phase tables unnecessarily.

---

# 91. Job Skill Table

The approved global architecture contains:

    job_skill

but do not populate it in Phase 10.14 through AI extraction.

It belongs to:

    Phase 10.16 JD Analysis

If the table is not yet needed, do not force its implementation into this phase.

---

# 92. Job Requirement Table

Same rule.

The approved architecture contains:

    job_requirement

but Phase 10.14 should not extract requirements.

Phase 10.16 owns this.

---

# 93. Migration

Create Alembic migrations for the foundational job domain.

At minimum:

    jobs
    job_sources
    job_locations

Include:

- foreign keys
- indexes
- constraints
- timestamps
- status fields

Do not modify unrelated tables unnecessarily.

---

# 94. Indexes

Useful indexes:

    jobs.company_id
    jobs.normalized_title
    jobs.status
    jobs.created_at
    jobs.last_seen_at
    jobs.workplace_mode
    jobs.employment_type

    job_sources.job_id
    job_sources.external_job_id
    job_sources.normalized_source_url

    job_locations.job_id
    job_locations.city
    job_locations.area

Create indexes based on actual expected queries.

---

# 95. Constraints

Useful uniqueness boundaries:

    provider + external_job_id

and/or:

    job_id + normalized_source_url

Do not create a global uniqueness constraint on:

    normalized_title

because many companies can have:

    Frontend Engineer

---

# 96. Job Source Provider Identity

A provider may return:

    external_job_id

Example:

    provider = linkedin
    external_job_id = 12345

Use the provider identity together with the external ID.

Do not assume external IDs are globally unique across providers.

---

# 97. Canonical Job Identity

Conceptually:

    provider + external_job_id
            ↓
        source identity
            ↓
       canonical job

Multiple source identities may point to:

    one canonical job

---

# 98. Job Description Hash

Optionally store a deterministic hash for change detection.

Example:

    description_hash

This can help identify whether the description changed.

Do not use the hash alone to determine job identity.

---

# 99. Job Change Detection

If a source returns the same job but description changed:

    same canonical job
        ↓
    update source data
        ↓
    update last_seen_at
        ↓
    preserve historical timestamps

Do not create a new job merely because the JD changed.

---

# 100. Job History

Full version history of job descriptions is not required in Phase 10.14.

If later needed:

    job_versions

can be introduced.

Do not overbuild now.

---

# 101. Acceptance Criteria

Phase 10.14 is complete only when:

- [ ] Canonical jobs can be stored.
- [ ] Jobs belong to companies.
- [ ] Multiple job sources are supported.
- [ ] Multiple job locations are supported.
- [ ] Job titles are normalized conservatively.
- [ ] Job source URLs are normalized.
- [ ] External job IDs are preserved.
- [ ] Job deduplication works.
- [ ] Repeated discovery does not create duplicates.
- [ ] Job status is tracked.
- [ ] Job freshness timestamps are tracked.
- [ ] Employment type is supported.
- [ ] Workplace mode is supported.
- [ ] Experience is supported.
- [ ] Salary is optional and never fabricated.
- [ ] User-provided job provider works.
- [ ] Job discovery provider abstraction exists.
- [ ] Company-specific source discovery is supported.
- [ ] Discovery API works.
- [ ] Job search API works.
- [ ] Job detail API works.
- [ ] Frontend job discovery UI works.
- [ ] External source URLs are visible.
- [ ] No job matching is implemented.
- [ ] No JD analysis is implemented.
- [ ] No resume tailoring is implemented.
- [ ] No applications are submitted.
- [ ] No unrestricted scraping is introduced.
- [ ] Backend tests pass.
- [ ] API tests pass.
- [ ] Frontend tests/build pass.
- [ ] Alembic migration passes.
- [ ] Existing phases remain functional.

---

# 102. Implementation Order

Implement sequentially:

1. Read this document completely.
2. Inspect Phase 10.12 implementation.
3. Inspect Phase 10.13 implementation.
4. Inspect existing provider architecture.
5. Inspect company models.
6. Inspect hiring-source models.
7. Inspect repository conventions.
8. Add Job model.
9. Add JobSource model.
10. Add JobLocation model.
11. Create Alembic migration.
12. Add job provider abstraction.
13. Add UserProvidedJobProvider.
14. Add job normalization.
15. Add job deduplication.
16. Add job repository.
17. Add job discovery service.
18. Add Pydantic schemas.
19. Add API endpoints.
20. Add frontend job service.
21. Add job discovery UI.
22. Add job detail UI.
23. Add backend unit tests.
24. Add provider tests.
25. Add deduplication tests.
26. Add API tests.
27. Add frontend tests/build.
28. Run migrations.
29. Run full test suite.
30. Inspect implementation.
31. Fix issues.
32. Verify architecture.
33. Produce final implementation report.

---

# 103. Codex Instructions

Implement ONLY Phase 10.14.

Before implementation:

- Read this document.
- Inspect Phase 10.12.
- Inspect Phase 10.13.
- Reuse existing company/hiring-source models.
- Reuse existing provider architecture.
- Reuse existing authentication.
- Reuse existing repository/schema conventions.
- Reuse existing discovery/search-run infrastructure where appropriate.

Do NOT:

- redesign previous phases
- implement Phase 10.15
- implement Phase 10.16
- implement Phase 10.17
- implement JD analysis
- implement matching
- implement resume selection
- implement resume tailoring
- implement applications
- implement outreach
- implement RAG
- implement Qdrant
- implement Gemini
- implement agents
- add browser automation
- add Playwright/Selenium
- add unrestricted scraping
- add paid services unless explicitly required by an already-approved architecture

The MVP must remain usable with manual/user-provided job data.

Do not fabricate job listings.

Do not fabricate salary information.

Do not fabricate company relationships.

Do not claim that a discovered job is a good match.

If a provider cannot reliably identify the company, do not automatically attach the job to a company.

If an architectural contradiction exists, explain it before making a major change.

---

# 104. Final Implementation Report

After implementation provide:

## Implemented

Exact functionality.

## Database

List:

- jobs
- job_sources
- job_locations

Include:

- fields
- relationships
- constraints
- indexes
- migrations

## Provider Architecture

Explain:

- provider interface
- user-provided provider
- normalization
- deduplication
- source identity

## APIs

List every endpoint.

## Frontend

Explain:

- job discovery
- job list
- job detail
- filters
- source display
- empty/loading/error states

## Security

Explain:

- authentication
- authorization
- company/job shared-data handling
- provider credential isolation
- URL safety
- external-content handling

## Tests

Provide actual results:

    Backend tests: X passed
    Provider tests: X passed
    API tests: X passed
    Frontend tests: X passed
    Angular build: PASS/FAIL
    Alembic migration: PASS/FAIL

## Warnings

List separately.

## Errors

List unresolved errors separately.

## Deviations

For every deviation:

    Expected:
    ...

    Implemented:
    ...

    Reason:
    ...

## Explicit Scope Check

Confirm:

    Phase 10.14 implemented: YES

    Phase 10.15:
    NOT IMPLEMENTED

    Phase 10.16 JD Analysis:
    NOT IMPLEMENTED

    Phase 10.17 Candidate Matching:
    NOT IMPLEMENTED

    Resume Selection:
    NOT IMPLEMENTED

    Resume Tailoring:
    NOT IMPLEMENTED

    Applications:
    NOT IMPLEMENTED

    Auto-Apply:
    NOT IMPLEMENTED