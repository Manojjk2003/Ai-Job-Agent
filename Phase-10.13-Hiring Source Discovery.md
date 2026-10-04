# Phase 10.13 — Hiring Source Discovery

## 1. Purpose

Phase 10.13 determines:

> Where does each company actually hire?

Phase 10.12 answered:

    "Which companies exist in/around the candidate's preferred location?"

Phase 10.13 answers:

    "Where can we find this company's hiring information?"

Example:

    Company:
    Example Technologies

    Hiring sources:
        Official Careers Page
        LinkedIn
        Indeed
        Wellfound
        Naukri
        Other permitted source

The system should not assume that every company uses every platform.

Instead, it should learn and store the hiring sources that are actually useful for each company.

---

# 2. Product Principle

The system should become company-aware.

Instead of:

    Search LinkedIn
    Search Naukri
    Search Indeed
    Search Wellfound

globally and hope for good results,

the system should reason:

    Company
       ↓
    Which hiring sources does this company use?
       ↓
    Verify source
       ↓
    Discover jobs from those sources

This creates the foundation for Phase 10.14 Job Discovery.

---

# 3. Important Distinction

Company Discovery:

    "This company exists in HSR Layout."

Hiring Source Discovery:

    "This company has a careers page and appears to hire through LinkedIn."

Job Discovery:

    "This company currently has a Frontend Engineer opening."

These are three separate domains.

Do not combine them.

---

# 4. Scope

Phase 10.13 includes:

- HiringSource model
- Company ↔ HiringSource relationship
- Hiring source types
- Source URL
- Source verification
- Source status
- Last verified timestamp
- Source confidence
- Provider abstraction
- Official career page discovery
- Permitted/user-provided source discovery
- Source normalization
- Duplicate prevention
- Company-specific source intelligence
- APIs
- Frontend hiring-source display
- Tests

---

# 5. Explicitly NOT Included

Do NOT implement:

- Job discovery
- Job scraping
- Job normalization
- JD parsing
- Candidate-job matching
- Resume tailoring
- Applications
- Outreach
- Automated applications
- Browser automation
- LinkedIn automation
- Naukri automation
- Indeed automation
- Wellfound automation
- RAG
- Qdrant
- Gemini
- Career Agent orchestration

Those belong to later phases.

---

# 6. Relationship With Previous Phase

The pipeline is now:

    Candidate
        ↓
    Preferences
        ↓
    Preferred Location
        ↓
    Company Discovery
        ↓
    Canonical Company
        ↓
    Hiring Source Discovery
        ↓
    Verified Hiring Sources
        ↓
    Job Discovery
        ↓
    Current Jobs

Phase 10.13 must consume the canonical companies created by Phase 10.12.

---

# 7. Core Data Model

A company can have multiple hiring sources.

Example:

    Company A
       |
       +---- Official Careers
       |
       +---- LinkedIn
       |
       +---- Indeed
       |
       +---- Wellfound

Therefore:

    Company
       ↕
    CompanyHiringSource
       ↕
    HiringSource

This is a many-to-many relationship.

---

# 8. Hiring Source

Create:

    hiring_sources

Recommended fields:

    id
    name
    normalized_name
    source_type
    base_url
    description
    is_active
    created_at
    updated_at

Examples:

    Official Careers
    LinkedIn
    Naukri
    Indeed
    Wellfound
    Company Website
    User Provided

---

# 9. Hiring Source Type

Use controlled values.

Example:

    official_careers
    company_website
    job_board
    professional_network
    startup_job_board
    aggregator
    user_provided
    other

Do not hard-code business logic around specific website names.

The type describes the source category.

---

# 10. Company Hiring Source

Create:

    company_hiring_sources

Recommended fields:

    id
    company_id
    hiring_source_id
    source_url
    external_reference
    status
    confidence
    discovery_method
    first_seen_at
    last_verified_at
    last_checked_at
    notes
    created_at
    updated_at

This represents:

> Company X uses Source Y at this URL.

---

# 11. Example

Company:

    Acme Technologies

Hiring source:

    Official Careers

Source URL:

    https://acme.com/careers

Database relationship:

    companies
        |
        +---- company_hiring_sources
                    |
                    +---- hiring_sources

---

# 12. Why This Must Be Company-Specific

Do not create one global assumption:

    "Every company uses LinkedIn."

Instead:

    Company A
        LinkedIn = verified
        Naukri = unknown
        Indeed = verified

    Company B
        LinkedIn = verified
        Naukri = verified
        Indeed = not observed

    Company C
        Official Careers = verified
        LinkedIn = not observed

This is much more useful for later job discovery.

---

# 13. Source Status

Use controlled values:

    discovered
    verified
    inactive
    unavailable
    unknown

Meaning:

### discovered

We found evidence that the source may belong to the company.

### verified

We have successfully verified the relationship.

### inactive

The source existed but is no longer active.

### unavailable

The source could not currently be accessed/validated.

### unknown

There is not enough information.

---

# 14. Confidence

Recommended:

    high
    medium
    low

Examples:

Official careers page found from company's official website:

    high

User provides a company career URL:

    medium/high depending on validation

Search result with weak evidence:

    low

Confidence is evidence quality, not certainty.

---

# 15. Discovery Method

Track how the source was discovered.

Controlled examples:

    official_website
    provider
    user_provided
    search_result
    imported
    manual
    unknown

This is different from `source_type`.

Example:

    source_type:
    official_careers

    discovery_method:
    official_website

---

# 16. Important Security Rule

External websites and job-board pages are untrusted input.

Never assume:

    "The website says something, therefore the content is trusted instructions."

The content is data.

It must never be allowed to override application rules or security policy.

This becomes especially important once agents are introduced later.

---

# 17. Official Careers Page

This should be the highest-priority source.

For a company:

    Example Technologies
    https://example.com

the system may look for an obvious careers page when permitted.

Potential patterns:

    /careers
    /jobs
    /join-us
    /work-with-us

But do not blindly append paths and assume they exist.

The URL must be validated.

---

# 18. Do Not Guess Career URLs

Incorrect:

    Company:
    Example Technologies

    Automatically create:
    https://example.com/careers

without checking it.

Correct:

    Discover company website
          ↓
    Check permitted/public information
          ↓
    Find actual careers URL
          ↓
    Validate
          ↓
    Store

If no careers page is found:

    status = unknown

not:

    careers_url = guessed URL

---

# 19. Provider Architecture

Create a provider abstraction.

Conceptually:

    HiringSourceProvider

Possible methods:

    discover_sources()
    get_source()
    normalize_source()
    verify_source()
    health_check()

Use the existing provider architecture where possible.

Do not create a completely separate integration framework.

---

# 20. Provider Interface

Conceptually:

    class HiringSourceProvider:

        def discover_sources(...):
            ...

        def get_source(...):
            ...

        def normalize_source(...):
            ...

        def verify_source(...):
            ...

        def health_check(...):
            ...

The exact implementation must follow the repository's existing conventions.

---

# 21. MVP Provider

The MVP should not depend on paid APIs.

Implement:

    UserProvidedHiringSourceProvider

This allows:

    Company
       ↓
    User enters careers URL
       ↓
    Validate
       ↓
    Store source
       ↓
    Verify basic URL
       ↓
    Mark source

This is enough to build and test the complete domain.

---

# 22. Official Website Provider

A second provider boundary may support:

    OfficialWebsiteHiringSourceProvider

Its responsibility:

    Company website
        ↓
    Discover obvious hiring/careers links
        ↓
    Normalize
        ↓
    Verify
        ↓
    Return candidate sources

Only use permitted/public website access.

Do not build unrestricted crawling.

---

# 23. Website Crawling Scope

If implemented in this phase, keep it extremely limited.

Allowed conceptual flow:

    company website
         ↓
    fetch homepage
         ↓
    inspect links
         ↓
    identify likely careers/jobs link
         ↓
    validate candidate URL

Do NOT recursively crawl the entire website.

Do NOT crawl unrelated pages.

Do NOT follow arbitrary external links.

---

# 24. Careers Link Detection

Potential link text:

    Careers
    Jobs
    Join Us
    Work With Us
    Open Positions
    Opportunities

This is heuristic discovery.

It is not proof.

The URL must still be validated.

---

# 25. External Hiring Sources

Potential sources may include:

    LinkedIn
    Naukri
    Indeed
    Wellfound
    Other permitted job boards

The architecture must not assume that unrestricted access to these platforms is available.

Each future integration must respect:

- API terms
- provider permissions
- authentication requirements
- rate limits
- robots/access policies
- applicable legal/platform restrictions

---

# 26. No Scraping-First Architecture

Do NOT implement:

    for every company:
        scrape LinkedIn
        scrape Naukri
        scrape Indeed
        scrape Wellfound

This is not the architecture.

Instead:

    Company
       ↓
    HiringSource Discovery
       ↓
    Provider abstraction
       ↓
    permitted source integrations
       ↓
    verified source records

---

# 27. Source URL Normalization

Normalize:

    https://www.example.com/careers/
    https://example.com/careers

where they represent the same URL.

Store the canonical URL while preserving useful source information.

Do not remove query parameters blindly when they may identify a valid source.

---

# 28. Domain Validation

For official careers sources, validate that the URL belongs to the company's known domain where appropriate.

Example:

    Company:
    example.com

Candidate careers URL:

    https://example.com/careers

Strong match.

But:

    https://random-job-site.com/acme

should not automatically be classified as:

    official_careers

It may instead be:

    job_board

---

# 29. Source Classification

Example:

    https://example.com/careers

    source_type:
    official_careers

Example:

    https://www.linkedin.com/company/example/jobs/

    source_type:
    professional_network

Example:

    https://www.naukri.com/example-jobs

    source_type:
    job_board

Classification should be provider-aware but represented canonically.

---

# 30. Company ↔ Source Uniqueness

Prevent duplicate relationships.

Do not create:

    Company A → LinkedIn

multiple times because discovery ran multiple times.

Use an appropriate uniqueness rule such as:

    company_id
    hiring_source_id
    normalized_source_url

or another stable identity combination.

---

# 31. Repeated Discovery

Suppose today's discovery finds:

    Acme → https://acme.com/careers

Tomorrow it finds the same URL.

The system should:

    UPDATE existing relationship

not:

    CREATE duplicate relationship

Update:

    last_seen_at
    last_checked_at
    last_verified_at

as appropriate.

---

# 32. Source Freshness

Store:

    first_seen_at
    last_checked_at
    last_verified_at

This enables future decisions such as:

    "This careers page was verified 2 days ago."

Do not imply that verification means jobs are currently available.

---

# 33. Hiring Source vs Job

A hiring source is not a job.

Example:

    https://acme.com/careers

is a hiring source.

Later:

    https://acme.com/careers/software-engineer-123

may be a specific job.

Phase 10.13 stores the first.

Phase 10.14 stores the second.

---

# 34. Hiring Source vs Company Website

A company website is not automatically a hiring source.

Example:

    https://acme.com

may be the company's website.

If it has:

    https://acme.com/careers

that can become:

    official_careers

Both can be represented separately if required.

---

# 35. Company Website Relationship

The company itself may already contain:

    website_url

from Phase 10.12.

Phase 10.13 uses this as an input.

Do not duplicate company website data unnecessarily.

---

# 36. Discovery Flow

Complete flow:

    Canonical Company
          ↓
    Company website
          ↓
    Hiring Source Provider(s)
          ↓
    Raw source candidates
          ↓
    Normalize
          ↓
    Classify
          ↓
    Verify
          ↓
    Deduplicate
          ↓
    company_hiring_sources
          ↓
    PostgreSQL

---

# 37. Discovery Service

Create:

    backend/app/services/hiring_source_discovery_service.py

Responsibilities:

- Accept company ID
- Validate company exists
- Resolve company website
- Select available providers
- Discover source candidates
- Normalize source records
- Classify source type
- Validate source URLs
- Deduplicate
- Upsert company-source relationships
- Update verification timestamps
- Return results

It must NOT discover jobs.

---

# 38. Repository

Create or extend:

    backend/app/repositories/hiring_source_repository.py

Responsibilities:

- Find hiring source
- Create hiring source
- Find company-source relationship
- Create relationship
- Update relationship
- List company sources
- Search source types
- Prevent duplicates

Keep database logic out of the service layer.

---

# 39. Schemas

Recommended:

    HiringSourceResponse
    CompanyHiringSourceResponse
    HiringSourceDiscoveryRequest
    HiringSourceDiscoveryResponse

Provider-specific schemas must not leak through the public API.

---

# 40. API Endpoints

Recommended:

    GET /api/v1/companies/{company_id}/hiring-sources

    POST /api/v1/companies/{company_id}/hiring-sources/discover

    POST /api/v1/companies/{company_id}/hiring-sources

    GET /api/v1/hiring-sources/{hiring_source_id}

The exact route style must follow existing project conventions.

---

# 41. Manual Source Creation

Example:

    POST /api/v1/companies/{company_id}/hiring-sources

Request:

    {
        "source_type": "official_careers",
        "source_url": "https://example.com/careers"
    }

Backend:

    authenticate
        ↓
    verify company
        ↓
    validate URL
        ↓
    normalize
        ↓
    deduplicate
        ↓
    store

---

# 42. Discovery Request

Example:

    POST /api/v1/companies/{company_id}/hiring-sources/discover

Request:

    {
        "providers": [
            "official_website"
        ]
    }

The backend may also use configured default providers.

Do not expose provider credentials.

---

# 43. Discovery Response

Example:

    {
        "company_id": "...",
        "status": "completed",
        "sources": [
            {
                "id": "...",
                "type": "official_careers",
                "url": "https://example.com/careers",
                "status": "verified",
                "confidence": "high"
            }
        ]
    }

---

# 44. No Job Count

Do NOT return:

    "12 jobs found"

because jobs are not part of Phase 10.13.

A source can exist even when it currently contains zero jobs.

---

# 45. Frontend Company Detail

The company detail page should now show:

    Example Technologies

    Website
    Location(s)

    Hiring Sources
    -----------------------------
    Official Careers
    Verified
    example.com/careers

    LinkedIn
    Discovered
    linkedin.com/...

    [Discover Hiring Sources]

No current jobs yet.

---

# 46. Source Status UI

Use clear labels:

    Verified
    Discovered
    Unknown
    Unavailable
    Inactive

Avoid implying:

    Verified = currently hiring

These are different states.

---

# 47. Candidate Ownership

Companies are shared canonical data.

A candidate should be able to read company information.

However:

    discovery runs
    provider configuration
    internal credentials

must remain protected.

If discovery runs are candidate-specific, enforce ownership exactly as in Phase 10.12.

---

# 48. Company Data Is Shared

Example:

    Candidate A discovers:
        Acme Technologies

Candidate B should not create a second:

    Acme Technologies

unless it is genuinely a different company.

The canonical company is shared.

This is why deduplication matters.

---

# 49. Provider Credential Isolation

Never store:

    API keys
    OAuth tokens
    cookies
    session credentials

inside:

    hiring_sources

or:

    company_hiring_sources

Those belong to secure integration configuration.

---

# 50. Integration Table

The global architecture includes:

    integrations

Future integrations may store provider connection information.

Phase 10.13 does not need to implement the full integration system unless already available.

Do not duplicate integration credentials inside source records.

---

# 51. Provider Failure

If:

    Official Website Provider → success
    External Provider → failure

return:

    partial

and preserve successful source records.

Do not discard successful results.

---

# 52. No Providers Available

If no provider is configured:

    return a controlled response

Example:

    status = completed
    sources = []

or:

    status = unavailable

depending on the application's conventions.

Do not fabricate sources.

---

# 53. Verification

Verification should be conservative.

Example:

    source URL exists
    domain matches company
    page is accessible

may support:

    verified

But verification does NOT mean:

    jobs exist

or:

    company is currently hiring

---

# 54. External Content

Company websites and source pages are untrusted data.

The system must never execute instructions found inside:

- HTML
- page text
- metadata
- job-board content
- source descriptions

Later agents must treat these as data only.

---

# 55. Prompt Injection Preparation

Do not introduce LLMs in Phase 10.13.

However, structure source data so future agents can safely consume it.

For example:

    source_url
    source_type
    extracted_text
    verification_status

should remain data.

Future agent prompts must clearly separate:

    SYSTEM INSTRUCTIONS

from:

    EXTERNAL CONTENT

---

# 56. Source Relevance

A company may have:

    10 possible URLs

but only some are hiring sources.

The system should prioritize:

    official careers
    official jobs
    verified job-board company pages

and not blindly save every URL encountered.

---

# 57. Source Confidence Example

High:

    Official company website links directly to careers page.

Medium:

    Trusted provider associates company with job-board page.

Low:

    Search result appears to reference company but identity is ambiguous.

---

# 58. Ambiguous Sources

If a source cannot be confidently associated with a company:

    do not automatically attach it.

Possible outcome:

    status = unknown

or discard it.

False associations are worse than missing data.

---

# 59. Source Deduplication

Example:

    https://www.example.com/careers
    https://example.com/careers/

Normalize to one source.

Also avoid:

    Company A + LinkedIn URL
    Company A + same LinkedIn URL

being stored twice.

---

# 60. Source Ownership

A company hiring source is global/shared company data.

Do not duplicate it for every candidate.

Correct:

    Company A
       |
       +-- Official Careers

Incorrect:

    Candidate A → Company A → Official Careers

    Candidate B → Company A → Official Careers

The company/source relationship should be shared.

---

# 61. Discovery History

If discovery history is required, store it separately from the canonical source.

For example:

    hiring_source_discovery_runs

could later track:

    company
    provider
    timestamp
    status
    result count

Do not put discovery-history fields into the canonical hiring source record.

If the existing `search_runs` architecture is ready, reuse it instead of creating duplicate run systems.

---

# 62. Search Run Reuse

The global architecture already contains:

    search_run

If Phase 10.12 implemented a reusable search-run model, extend it.

Example:

    search_type:
    hiring_source_discovery

Do not create competing:

    search_runs
    discovery_runs
    source_search_runs

unless there is a strong architectural reason.

---

# 63. Database Constraints

Recommended:

    hiring_sources.normalized_name
        appropriate uniqueness

    company_hiring_sources
        unique company/source/url relationship

Foreign keys:

    company_hiring_sources.company_id
        → companies.id

    company_hiring_sources.hiring_source_id
        → hiring_sources.id

Use cascade behavior carefully.

Do not delete historical source data accidentally when a company record is archived.

---

# 64. Indexes

Useful indexes:

    companies.id
    hiring_sources.source_type
    hiring_sources.normalized_name
    company_hiring_sources.company_id
    company_hiring_sources.hiring_source_id
    company_hiring_sources.status
    company_hiring_sources.last_verified_at

Follow actual query patterns rather than creating excessive indexes.

---

# 65. Migration

Create an Alembic migration.

Migration should:

- create hiring_sources
- create company_hiring_sources
- add foreign keys
- add constraints
- add indexes
- preserve existing company data
- be reversible where practical

Run:

    alembic upgrade head

and verify.

---

# 66. Seed Data

Seed common source definitions if appropriate:

    Official Careers
    Company Website
    LinkedIn
    Naukri
    Indeed
    Wellfound
    User Provided

These are source definitions only.

Do not create company relationships automatically.

Do not claim that every company uses them.

---

# 67. Seed Safety

If source definitions already exist:

    reuse them

Do not create duplicates every time the application starts.

Seed operations should be idempotent.

---

# 68. Testing — Unit Tests

Test:

- URL normalization
- domain extraction
- source classification
- source-type normalization
- deduplication
- confidence calculation
- provider normalization
- invalid URL rejection
- duplicate source prevention

---

# 69. Testing — Provider Tests

Mock external responses.

Do NOT depend on real external websites for unit tests.

Test:

    provider response
       ↓
    normalized source

including:

- valid careers page
- multiple links
- missing website
- malformed URL
- duplicate links
- provider error
- timeout

---

# 70. Testing — Service Tests

Test:

- valid company
- nonexistent company
- source discovery
- duplicate prevention
- multiple providers
- partial provider failure
- source update
- verification update
- no job discovery

---

# 71. Testing — API

Test:

    GET /companies/{id}/hiring-sources

    POST /companies/{id}/hiring-sources

    POST /companies/{id}/hiring-sources/discover

Test:

- authentication
- authorization
- validation
- successful response
- duplicate behavior
- nonexistent company
- provider failure

---

# 72. Testing — Security

Verify:

- unauthenticated requests rejected
- invalid Firebase token rejected
- provider credentials never returned
- cross-candidate discovery data protected
- company IDs validated
- unsafe URLs rejected where required
- no secrets logged

---

# 73. Testing — Existing Features

After implementation verify that previous phases still work:

    Candidate onboarding
    Candidate profile
    Skills
    Resume upload
    Resume parsing
    Role profiles
    Candidate preferences
    Company discovery

No regression should be introduced.

---

# 74. Frontend Tests

Test:

- source list rendering
- empty state
- loading state
- error state
- discover action
- manual source addition
- duplicate handling
- source status display

---

# 75. Frontend UX

Empty state:

    "No hiring sources discovered yet."

Action:

    [Discover Hiring Sources]

If none are found:

    "We couldn't verify a hiring source for this company yet."

Do not say:

    "This company doesn't hire."

That conclusion is unsupported.

---

# 76. Important Product Language

Correct:

    "No hiring source found."

Incorrect:

    "Company is not hiring."

Correct:

    "No current openings found."

Incorrect:

    "Company has no jobs."

The distinction will become important in Phase 10.14.

---

# 77. Example End-to-End Flow

Candidate:

    "Find companies around HSR Layout."

Phase 10.12:

    HSR Layout
       ↓
    Acme Technologies
    Example Labs
    XYZ Systems

Candidate selects:

    Acme Technologies

Phase 10.13:

    Acme Technologies
       ↓
    Official Website
       ↓
    Careers Page
       ↓
    LinkedIn
       ↓
    Other permitted sources

Result:

    Acme Technologies
       |
       +-- Official Careers — Verified
       +-- LinkedIn — Discovered
       +-- Indeed — Unknown

Phase 10.14 will later use these sources to find actual jobs.

---

# 78. Why This Architecture Matters

Later the system can learn:

    Company A:
        Official Careers → high value
        LinkedIn → high value
        Naukri → low value

    Company B:
        Naukri → high value
        Indeed → high value

    Company C:
        Official Careers → only useful source

This can improve job-discovery efficiency.

But do NOT implement learning/ranking automation in this phase.

---

# 79. No AI Required

Phase 10.13 should work without Gemini.

The initial flow is deterministic:

    Provider
       ↓
    Normalize
       ↓
    Validate
       ↓
    Deduplicate
       ↓
    Store

AI may be useful later for:

- ambiguous source classification
- company intelligence
- source relevance
- natural-language reasoning

but it is not required for this domain foundation.

---

# 80. No Qdrant Required

Hiring source records are structured relational data.

Store them in PostgreSQL.

Do not create embeddings for:

    hiring_source
    source_url
    company-source relationship

during this phase.

---

# 81. No RAG Required

RAG begins later when the system needs semantic retrieval over:

- resumes
- candidate profiles
- projects
- jobs
- company information
- JDs

Hiring-source relationships are primarily structured data.

---

# 82. Acceptance Criteria

Phase 10.13 is complete only when:

- [ ] HiringSource model exists.
- [ ] CompanyHiringSource relationship exists.
- [ ] Multiple sources per company are supported.
- [ ] Source types are controlled.
- [ ] Source URLs are normalized.
- [ ] Source duplication is prevented.
- [ ] Source status is tracked.
- [ ] Source confidence is tracked.
- [ ] First-seen timestamp is stored.
- [ ] Last-checked timestamp is stored.
- [ ] Last-verified timestamp is stored.
- [ ] Discovery method is stored.
- [ ] Provider abstraction exists.
- [ ] User-provided source provider works.
- [ ] Official website discovery boundary exists if implemented.
- [ ] No unrestricted scraping is introduced.
- [ ] No job discovery is implemented.
- [ ] No job matching is implemented.
- [ ] No AI dependency is introduced.
- [ ] Company ownership/shared-data rules are respected.
- [ ] API endpoints work.
- [ ] Frontend company source UI works.
- [ ] Unit tests pass.
- [ ] Provider tests pass.
- [ ] API tests pass.
- [ ] Frontend build/tests pass.
- [ ] Alembic migration passes.
- [ ] Existing phases remain functional.

---

# 83. Implementation Order

Implement sequentially:

1. Read this document completely.
2. Inspect Phase 10.12 implementation.
3. Inspect the existing provider architecture.
4. Inspect company models and repositories.
5. Inspect API conventions.
6. Inspect authentication.
7. Add HiringSource model.
8. Add CompanyHiringSource model.
9. Add migration.
10. Seed canonical source definitions where appropriate.
11. Add source normalization utilities.
12. Add provider interface.
13. Add UserProvidedHiringSourceProvider.
14. Add official website provider boundary if supported by the existing HTTP architecture.
15. Add hiring-source repository.
16. Add hiring-source discovery service.
17. Add Pydantic schemas.
18. Add API endpoints.
19. Add frontend service.
20. Add company hiring-source UI.
21. Add manual source creation UI if appropriate.
22. Add unit tests.
23. Add provider tests.
24. Add service tests.
25. Add API tests.
26. Add frontend tests/build.
27. Run Alembic migrations.
28. Run complete test suite.
29. Inspect implementation.
30. Fix issues.
31. Verify architecture.
32. Produce final implementation report.

---

# 84. Codex Instructions

Implement ONLY Phase 10.13.

Before implementation:

- Read this document.
- Inspect Phase 10.12 implementation.
- Reuse the existing company model.
- Reuse existing authentication.
- Reuse existing provider conventions.
- Reuse existing search-run infrastructure if already implemented.
- Reuse existing API/schema/repository conventions.

Do NOT:

- redesign Phase 10.12
- implement Phase 10.14
- implement job discovery
- scrape LinkedIn
- scrape Naukri
- scrape Indeed
- scrape Wellfound
- use browser automation
- add Playwright/Selenium
- add Gemini
- add Qdrant
- add RAG
- add Redis
- add Celery
- add Kafka
- build an unrestricted crawler

The MVP must remain usable without paid external APIs.

Use manual/user-provided sources to prove the complete domain.

If official website discovery is implemented, keep it limited to permitted/public website access and a narrow discovery flow.

Do not invent hiring sources.

Do not claim that a company is hiring merely because a hiring source exists.

If an architectural contradiction is found, report it before making a major architectural change.

---

# 85. Final Implementation Report

After implementation provide:

## Implemented

Exact functionality.

## Database

List:

- hiring_sources
- company_hiring_sources
- fields
- relationships
- constraints
- indexes
- migrations

## Provider Architecture

Explain:

- provider interface
- user-provided provider
- official website provider if implemented
- normalization
- validation
- deduplication

## APIs

List every endpoint.

## Frontend

Explain:

- company hiring-source section
- source status
- discovery action
- manual source addition
- empty/loading/error states

## Security

Explain:

- authentication
- authorization
- shared company data
- candidate-specific discovery data
- credential isolation
- URL validation

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

    Phase 10.13 implemented: YES

    Phase 10.14 Job Discovery:
    NOT IMPLEMENTED

    Job scraping:
    NOT IMPLEMENTED

    Job matching:
    NOT IMPLEMENTED

    Resume tailoring:
    NOT IMPLEMENTED

    Applications:
    NOT IMPLEMENTED