Phase 10.12 — Company Discovery
# Phase 10.12 — Company Discovery

## 1. Purpose

Phase 10.12 introduces the first major discovery capability of the product:

> Discover companies relevant to a candidate's preferred locations and career goals.

The product should not begin with:

    "Search for jobs everywhere."

Instead, the core discovery flow is:

    Candidate Preferences
            ↓
    Preferred Location / Area
            ↓
    Discover Relevant Companies
            ↓
    Store Canonical Companies
            ↓
    Store Company Locations
            ↓
    Verify Company Information
            ↓
    Later: Discover Hiring Sources
            ↓
    Later: Discover Jobs

This phase creates the company foundation required by the later hiring-source and job-discovery phases.

---

# 2. Core Product Principle

The product's differentiation is:

> Find the companies, not just the jobs.

For example, a candidate may select:

    HSR Layout, Bangalore

The future system should be able to reason:

    HSR Layout
       ↓
    Companies in/around HSR Layout
       ↓
    Company websites
       ↓
    Company career pages
       ↓
    Hiring sources
       ↓
    Current openings

Phase 10.12 stops at:

    Relevant Companies

It does NOT discover jobs yet.

---

# 3. Critical Architecture Rule

Do not build the company-discovery system around unrestricted scraping.

The system must be provider-agnostic.

Possible future sources include:

- Official company websites
- Official company career pages
- Permitted company/business APIs
- User-provided company lists
- Approved external providers
- Other sources where access is permitted

Do NOT assume that the system can freely scrape:

- Google Maps
- LinkedIn
- Naukri
- Indeed
- Wellfound
- other protected platforms

The discovery architecture must work even when one provider is unavailable.

---

# 4. Scope

Phase 10.12 includes:

- Company model
- Company location model
- Canonical company records
- Company discovery abstraction
- Company provider interface
- Manual/user-provided company discovery
- Provider result normalization
- Company deduplication
- Company-location association
- Discovery runs
- Discovery status
- Discovery confidence
- Basic company metadata
- Candidate/location-based discovery API
- Company listing/search API
- Frontend company-discovery UI
- Candidate ownership/security where applicable
- Tests

---

# 5. Explicitly NOT Included

Do NOT implement:

- Hiring source discovery
- Job discovery
- Job scraping
- Job matching
- JD analysis
- Resume tailoring
- Application automation
- Contact discovery
- Recruiter discovery
- Outreach
- Agent orchestration
- RAG
- Qdrant indexing
- Automatic applications
- LinkedIn automation
- Naukri automation
- Google Maps scraping
- Browser automation
- unrestricted web scraping

Those belong to later phases.

---

# 6. Relationship With Previous Phases

Current sequence:

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
          ↓
    10.11 Preferences
          ↓
    10.12 Company Discovery
          ↓
    10.13 Hiring Source Discovery
          ↓
    10.14 Job Discovery

Phase 10.12 consumes:

- Candidate preferences
- Preferred locations
- Candidate role context

and produces:

- Canonical companies
- Company locations
- Company discovery records

---

# 7. Why Company Discovery Comes Before Job Discovery

The product should eventually support:

    "Find frontend jobs around HSR Layout."

A generic job search would do:

    HSR Layout
       ↓
    Job Search API
       ↓
    Jobs

Our architecture should be capable of:

    HSR Layout
       ↓
    Companies
       ↓
    Company websites
       ↓
    Hiring sources
       ↓
    Jobs

This enables the product to understand:

- which companies are actually in the area
- which companies are relevant
- where each company hires
- which sources are useful for that company
- whether a company has a direct careers page
- how fresh the company's hiring information is

That intelligence becomes valuable later.

---

# 8. Company as a Canonical Entity

A company should exist only once in the canonical database.

For example:

    Acme Technologies

might appear in:

- Company website
- LinkedIn
- Indeed
- Wellfound
- Naukri
- user-provided data

These should not create six companies.

Instead:

    Canonical Company
          │
          ├── Company Source A
          ├── Company Source B
          ├── Company Source C
          └── Company Source D

Source-specific information belongs in later source/provider structures.

---

# 9. Company Table

Create:

    companies

Recommended fields:

    id
    canonical_name
    normalized_name
    legal_name
    website_url
    linkedin_url
    description
    industry
    company_size
    company_stage
    logo_url
    headquarters_location_id
    status
    confidence
    created_at
    updated_at

Not every field needs to be populated during discovery.

The system must distinguish:

    known
    unknown

from:

    guessed

Do not invent company information.

---

# 10. Canonical Name

Example:

    "Acme Technologies Pvt. Ltd."

may have:

    canonical_name:
    Acme Technologies

The canonical name is the application-facing company identity.

Do not arbitrarily remove meaningful company distinctions.

For example:

    ABC Technologies
    ABC Technologies Labs

should not automatically be merged merely because their names look similar.

---

# 11. Normalized Name

Store a normalized value for duplicate detection.

Example:

    canonical_name:
    Acme Technologies

    normalized_name:
    acme technologies

Normalization may include:

- lowercase
- whitespace normalization
- punctuation normalization
- safe suffix normalization where appropriate

Do not perform aggressive fuzzy matching using only names.

---

# 12. Company Identity

Company identity should eventually use multiple signals.

Possible identity signals:

    normalized name
    official website domain
    external provider ID
    LinkedIn company URL
    known legal name
    source URL

The official website domain is particularly useful.

Example:

    https://acme.com

should strongly suggest:

    acme.com

is the company's canonical domain.

---

# 13. Unique Website Domain

Where possible, extract the normalized domain:

    acme.com

rather than storing only:

    https://www.acme.com/

This helps deduplicate:

    https://acme.com
    https://www.acme.com/
    http://acme.com/

The database may store the original website URL separately.

---

# 14. Company Status

Use a controlled status:

    active
    inactive
    unknown

Do not mark a company inactive merely because no job was found.

A company may have no current opening while still being active.

---

# 15. Company Confidence

Discovery results may have different levels of reliability.

Recommended:

    high
    medium
    low

Example:

    Official company website
        → high

    Trusted structured provider
        → medium/high

    User-provided company
        → medium/high depending on validation

    Weak name-only result
        → low

Do not treat confidence as truth.

It represents confidence in the discovered company record.

---

# 16. Company Location

Create:

    company_locations

Recommended fields:

    id
    company_id
    location_name
    area
    city
    state
    country
    postal_code
    latitude
    longitude
    location_type
    is_headquarters
    is_verified
    confidence
    source
    created_at
    updated_at

Latitude/longitude may remain NULL in MVP.

Do not require geocoding in this phase.

---

# 17. Location Type

Controlled values may include:

    headquarters
    office
    branch
    remote
    unknown

A company may have multiple locations.

Example:

    Company A
       |
       +-- Bangalore
       +-- Mumbai
       +-- Pune

---

# 18. Why Company Locations Need Their Own Table

Do NOT put:

    city = Bangalore

directly inside `companies`.

A company may have:

    Bangalore
    Mumbai
    Chennai

Therefore:

    companies
         |
         +---- company_locations

is required.

---

# 19. Area-Level Location

Company discovery should support area-level information when available.

Example:

    HSR Layout
    Koramangala
    Whitefield
    Indiranagar

Store:

    area = HSR Layout
    city = Bangalore
    state = Karnataka
    country = India

Do not attempt geographic calculations in this phase.

---

# 20. Company Discovery Provider

Create a provider abstraction.

Conceptual interface:

    CompanyDiscoveryProvider

with operations such as:

    search_companies()
    get_company()
    normalize_company()
    health_check()

The provider must return normalized discovery results.

---

# 21. Why Provider Abstraction Is Required

The product must not depend permanently on one source.

Architecture:

    Company Discovery Service
            |
            +---- Provider A
            |
            +---- Provider B
            |
            +---- User Provided Provider
            |
            +---- Official Website Provider
            |
            +---- Future Provider

If one provider stops working, the rest of the application should remain functional.

---

# 22. Provider Interface

Conceptually:

    class CompanyDiscoveryProvider:

        def search_companies(...):
            ...

        def get_company(...):
            ...

        def normalize_company(...):
            ...

        def health_check(...):
            ...

The exact Python interface should follow the existing provider architecture.

Do not invent a second provider framework if one already exists in the repository.

---

# 23. MVP Provider

Because this is a local/free MVP, implement a provider that does not require a paid external API.

Recommended:

    UserProvidedCompanyProvider

It can accept company data from:

- candidate-provided input
- imported company lists
- manually entered companies
- future approved sources

This lets us build and test the entire company domain without making the MVP dependent on a paid API.

---

# 24. Future Providers

The architecture should allow:

    OfficialWebsiteCompanyProvider
    PermittedBusinessDirectoryProvider
    ApprovedCompanyAPIProvider
    UserProvidedCompanyProvider

Later, additional providers can be added where access is permitted.

Do not implement all providers now.

---

# 25. User-Provided Company Flow

Example:

Candidate enters:

    Company:
    Example Technologies

    Website:
    https://example.com

    Location:
    HSR Layout, Bangalore

Backend:

    Validate
       ↓
    Normalize
       ↓
    Deduplicate
       ↓
    Create/update company
       ↓
    Create company location
       ↓
    Return canonical company

This provides a working discovery path without scraping.

---

# 26. Discovery Run

Create a record of discovery operations.

Recommended table:

    company_discovery_runs

Fields:

    id
    candidate_id
    query
    location
    provider_name
    status
    started_at
    completed_at
    result_count
    error_message
    created_at

This gives the system an audit trail.

---

# 27. Why Discovery Runs Matter

Later we need to answer:

    "When did we search HSR Layout?"

    "Which provider produced this company?"

    "Was this result found yesterday or today?"

    "Did the provider fail?"

    "How many companies were discovered?"

Without discovery-run data, this becomes difficult.

---

# 28. Discovery Status

Use:

    pending
    running
    completed
    failed
    partial

`partial` is important.

For example:

    Provider A succeeded
    Provider B failed

The overall discovery operation may still return useful companies.

Do not treat one provider failure as total discovery failure.

---

# 29. Company Discovery Source

For MVP, preserve where the company came from.

Possible:

    user_provided
    official_website
    provider
    imported
    unknown

Do not use a free-form source string everywhere if a controlled provider architecture already exists.

---

# 30. Company Source Record

A future source model may be:

    company_sources

However, Phase 10.12 should not duplicate the Phase 10.13 hiring-source domain.

Important distinction:

Company source:

    "Where did we learn this company exists?"

Hiring source:

    "Where does this company actually hire?"

These are different.

Do not combine them.

---

# 31. Company Discovery vs Hiring Source Discovery

Company Discovery:

    "Acme exists in HSR Layout."

Hiring Source Discovery:

    "Acme hires through its careers page and LinkedIn."

Job Discovery:

    "Acme currently has a Full Stack Engineer opening."

Keep these separate.

---

# 32. Candidate Discovery Request

The API should eventually support:

    POST /api/v1/companies/discover

Example request:

    {
        "location": {
            "area": "HSR Layout",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "India"
        }
    }

The backend determines the authenticated candidate.

Do not accept candidate_id from the browser.

---

# 33. Discovery Options

Optional request fields:

    role_profile_id
    radius
    max_results
    providers

But do not implement geographic radius calculations yet unless an approved provider supports them.

For MVP:

    location
    max_results

are enough.

---

# 34. Role Profile During Discovery

A role profile may be supplied to improve relevance.

Example:

    role_profile_id:
    Frontend Engineer

This can later allow the system to prioritize companies likely to employ frontend engineers.

However, Phase 10.12 should not perform job matching.

It may simply preserve the role context in the discovery run.

---

# 35. Preference-Based Discovery

If the candidate does not provide a location explicitly, the backend may use:

    candidate_preferences

to retrieve preferred locations.

Example:

    Candidate Preferences
         ↓
    Primary Location
         ↓
    Company Discovery

This is useful for the eventual assistant.

---

# 36. Example User Flow

User:

    "Find companies around HSR Layout."

Backend:

    authenticated candidate
         ↓
    preference lookup
         ↓
    HSR Layout
         ↓
    CompanyDiscoveryService
         ↓
    Provider(s)
         ↓
    Normalize results
         ↓
    Deduplicate
         ↓
    Save companies
         ↓
    Save company locations
         ↓
    Return companies

---

# 37. Company Discovery Service

Create:

    backend/app/services/company_discovery_service.py

Responsibilities:

- Validate discovery request
- Resolve candidate
- Resolve location
- Select providers
- Execute provider searches
- Normalize results
- Deduplicate companies
- Upsert canonical companies
- Upsert company locations
- Record discovery run
- Return results

It must not:

- discover jobs
- discover hiring sources
- perform resume matching
- call Gemini
- index Qdrant

---

# 38. Company Repository

Create:

    backend/app/repositories/company_repository.py

Responsibilities:

- Find company
- Create company
- Update company
- Find by normalized name
- Find by website domain
- Create/update locations
- Search companies
- List companies

Repository must remain database-focused.

---

# 39. Provider Directory

Possible structure:

    backend/app/providers/
        company/
            __init__.py
            base.py
            user_provided.py

If the repository already has a provider structure, extend it instead.

Do not create competing provider conventions.

---

# 40. Schemas

Add schemas such as:

    CompanyResponse
    CompanyLocationResponse
    CompanyDiscoveryRequest
    CompanyDiscoveryResponse
    CompanyDiscoveryRunResponse

Provider-specific schemas should not leak directly into public API contracts.

---

# 41. Company API

Recommended endpoints:

    GET /api/v1/companies
    GET /api/v1/companies/{company_id}
    POST /api/v1/companies
    PUT /api/v1/companies/{company_id}

These allow canonical company management.

For discovery:

    POST /api/v1/companies/discover

For discovery runs:

    GET /api/v1/companies/discovery-runs
    GET /api/v1/companies/discovery-runs/{run_id}

---

# 42. Company Location API

Recommended:

    GET /api/v1/companies/{company_id}/locations
    POST /api/v1/companies/{company_id}/locations

Updating/deleting locations should only be exposed if required by the UI.

Do not create unnecessary APIs.

---

# 43. Company Creation

Example:

    POST /api/v1/companies

Request:

    {
        "name": "Example Technologies",
        "website_url": "https://example.com"
    }

The backend:

    normalize
        ↓
    deduplicate
        ↓
    create/update canonical company

---

# 44. Company Discovery Response

Example:

    {
        "run_id": "uuid",
        "status": "completed",
        "location": {
            "area": "HSR Layout",
            "city": "Bangalore"
        },
        "companies": [
            {
                "id": "uuid",
                "name": "Example Technologies",
                "website_url": "https://example.com",
                "confidence": "high"
            }
        ]
    }

The API should not claim:

    "This company is hiring."

unless a later hiring-source/job phase has established that.

---

# 45. Important Language Rule

Company discovery must not imply job availability.

Correct:

    "Company discovered in HSR Layout."

Incorrect:

    "Company has open jobs."

The second statement belongs to Job Discovery.

---

# 46. Deduplication

Deduplication is one of the most important parts of this phase.

Suppose providers return:

    Example Technologies
    Example Technologies Pvt Ltd
    EXAMPLE TECHNOLOGIES

with:

    example.com

These should potentially resolve to one company.

Use identity signals in order of strength.

---

# 47. Deduplication Priority

Strongest signals:

1. Exact official website domain
2. Provider external company ID
3. Exact normalized domain
4. Known canonical identifier
5. Strong normalized-name match
6. Name + location similarity

Never merge companies solely because their names are similar when confidence is low.

---

# 48. Website Domain Deduplication

Example:

    https://www.example.com
    https://example.com/careers
    http://example.com/

all point to:

    example.com

They should resolve to the same canonical company when other signals support it.

---

# 49. Name Deduplication

Normalize:

    Example Technologies Pvt. Ltd.

to something like:

    example technologies

but do not remove arbitrary words without a controlled normalization strategy.

Avoid aggressive transformations that could merge unrelated companies.

---

# 50. Fuzzy Matching

Do NOT automatically perform fuzzy company merging in the first implementation.

Fuzzy matching can create serious false positives.

For example:

    ABC Solutions
    ABC Solution Labs
    ABC Technologies

may be different companies.

MVP should prefer conservative matching.

---

# 51. Company Confidence

Example:

Provider returns:

    name = Example Technologies
    website = example.com
    city = Bangalore

Confidence:

    high

Provider returns:

    name = Example Technologies
    no website
    no location

Confidence:

    low/medium

Confidence should be derived from evidence available at discovery time.

---

# 52. Company Location Deduplication

A company may receive:

    HSR Layout
    HSR Layout, Bangalore
    HSR Layout, Bengaluru

Normalize the location carefully.

Do not create duplicate company-location records when they clearly represent the same office.

---

# 53. Bengaluru vs Bangalore

Location normalization should support aliases.

For example:

    Bangalore
    Bengaluru

may represent the same city.

However, this does not mean the system should globally hard-code every geographic alias.

A later location-intelligence layer can provide canonical geographic entities.

For MVP, use a simple normalization mapping only where required.

---

# 54. Company Search API

`GET /api/v1/companies`

may support:

    search
    city
    area
    status
    limit
    offset

Example:

    GET /api/v1/companies?search=example&city=Bangalore

The API must only return canonical companies.

---

# 55. Company Detail

Company detail should show:

    Company Name
    Website
    Description
    Industry
    Company Size
    Company Stage
    Locations
    Confidence
    Last Updated

Do not show:

    Current Jobs

because Job Discovery has not happened yet.

---

# 56. Frontend Company Discovery Page

Recommended UI:

    Company Discovery

    Search location:
    [ HSR Layout, Bangalore ]

    [Discover Companies]

    --------------------------------

    Companies Found

    Example Technologies
    HSR Layout, Bangalore
    Website: example.com
    Confidence: High

    [View]

    --------------------------------

    Another Company
    Koramangala, Bangalore

    [View]

---

# 57. Discovery Run UI

Show useful status:

    Discovering companies...

    Provider:
    User Provided

    Status:
    Completed

    Companies found:
    18

Do not expose internal implementation details unnecessarily.

---

# 58. No Fake Results

The application must never fabricate companies just to make the UI look populated.

If the MVP provider has no data:

    0 companies found

is correct.

Do not generate fake company records.

---

# 59. Provider Failure

Suppose:

    Provider A → success
    Provider B → failure

The system should return:

    status = partial

with the successful results.

The error should be recorded in the discovery run.

---

# 60. Provider Timeout

Provider calls must have controlled timeouts.

Do not allow one external provider to block the entire request indefinitely.

Use the project's existing `httpx`/HTTP configuration if applicable.

---

# 61. Provider Rate Limits

Do not implement aggressive retry loops.

Future providers must respect:

- provider rate limits
- terms of service
- API quotas
- robots/access restrictions where applicable

MVP user-provided discovery does not require external retries.

---

# 62. Security

Company data may be public, but discovery operations are still application actions.

Protect:

- candidate-specific discovery runs
- provider credentials
- internal provider configuration
- API keys
- logs

Never expose provider credentials to Angular.

---

# 63. Provider Credentials

Future provider credentials must be stored server-side.

Never:

    Angular
       ↓
    API key

Instead:

    Angular
       ↓
    FastAPI
       ↓
    Provider
       ↓
    Credential stored securely

No provider secrets in Git.

---

# 64. Auditability

A discovery run should preserve:

    candidate
    location
    provider
    query
    time
    status
    result count
    errors

This will later help analyze:

    Which provider is useful?
    Which locations produce results?
    Which companies are repeatedly discovered?

---

# 65. Company Freshness

Store:

    created_at
    updated_at

Discovery runs store their own timestamps.

Do not claim that a company is currently operating at a location merely because an old discovery record exists.

Later freshness rules can be introduced.

---

# 66. Company Metadata

The system may receive:

    industry
    employee count
    stage
    description

but these fields may be unknown.

Represent unknown as:

    NULL / unknown

not:

    "Not available" fake data

and definitely not guessed values.

---

# 67. Official Website

If a company has a website:

    website_url

should be stored.

Prefer canonical HTTPS URL.

Do not automatically assume:

    companyname.com

without evidence.

---

# 68. Company Website Verification

Phase 10.12 may validate basic URL syntax.

It does not need to deeply crawl or verify the website.

Later hiring-source discovery can inspect the official website.

---

# 69. Company Domain

Store a normalized domain separately if useful:

    website_domain

Example:

    example.com

This is useful for deduplication and later company intelligence.

---

# 70. Company Logo

Logo support is optional.

Do not fetch logos from random services in this phase.

If a provider gives a logo URL, store it only if permitted and safe.

The frontend must gracefully handle missing logos.

---

# 71. Company Description

Descriptions should be sourced from:

- company-provided information
- permitted provider data
- user input

Do not ask Gemini to invent company descriptions.

---

# 72. Role Relevance

Phase 10.12 should NOT calculate:

    Frontend relevance = 87%

That is job/candidate matching territory.

However, a discovery request may preserve:

    role_profile_id

so later analysis can understand why the company was discovered.

---

# 73. Location Relevance

At this stage, company discovery should establish:

    company location

not:

    candidate-location score

Later matching/location intelligence can calculate:

    exact area
    nearby
    same city
    remote
    relocation

---

# 74. Future Location Intelligence

Later architecture may become:

    Candidate Location
           ↓
    Location Intelligence
           ↓
    Company Location
           ↓
    distance / area relationship

Potential future technologies:

- PostGIS
- geocoding provider
- geographic APIs

Do not implement these now.

---

# 75. Data Flow

Complete Phase 10.12:

    Candidate
        ↓
    Preferences
        ↓
    Preferred Location
        ↓
    Company Discovery Request
        ↓
    CompanyDiscoveryService
        ↓
    Provider(s)
        ↓
    Raw Results
        ↓
    Normalize
        ↓
    Deduplicate
        ↓
    Canonical Company
        ↓
    Company Location
        ↓
    PostgreSQL
        ↓
    Company Discovery UI

---

# 76. Backend Structure

Possible additions:

    backend/app/
    ├── api/
    │   └── v1/
    │       └── companies.py
    │
    ├── providers/
    │   └── company/
    │       ├── __init__.py
    │       ├── base.py
    │       └── user_provided.py
    │
    ├── repositories/
    │   ├── company_repository.py
    │   └── company_discovery_repository.py
    │
    ├── schemas/
    │   └── company.py
    │
    └── services/
        └── company_discovery_service.py

Follow existing repository conventions.

---

# 77. Database Tables

At minimum:

    companies
    company_locations
    company_discovery_runs

Potential future tables:

    company_sources
    company_hiring_sources

Do NOT add hiring-source tables in this phase unless already required by the approved schema.

---

# 78. Company Discovery Run Relationship

Recommended:

    Candidate
        |
        +---- CompanyDiscoveryRun
                     |
                     +---- discovered companies

The run does not necessarily need a many-to-many join table for MVP if results are simply persisted as canonical companies.

If historical result membership is required, a later table can be introduced:

    company_discovery_run_results

Do not add unnecessary complexity unless the implementation needs it.

---

# 79. Optional Run Result Table

If the implementation requires exact historical result tracking, create:

    company_discovery_run_results

Fields:

    id
    discovery_run_id
    company_id
    provider_name
    provider_company_id
    confidence
    created_at

This is useful because the same company may be returned by multiple discovery runs.

If this table is implemented, use it consistently.

---

# 80. Provider Result

Internal normalized provider result:

    {
        "external_id": "...",
        "name": "...",
        "website_url": "...",
        "description": "...",
        "industry": "...",
        "locations": [
            {
                "area": "...",
                "city": "...",
                "state": "...",
                "country": "..."
            }
        ],
        "source": "..."
    }

The exact schema should remain provider-independent.

---

# 81. Provider Independence

Do not allow this:

    Company model
        ↓
    LinkedIn-specific fields everywhere

or:

    Company model
        ↓
    Naukri-specific assumptions

Provider-specific fields should remain inside provider/source structures.

The canonical company domain should represent the company itself.

---

# 82. Manual Company Creation

The user should be able to manually add a company.

Example:

    [+ Add Company]

    Company Name:
    Example Technologies

    Website:
    https://example.com

    Location:
    HSR Layout, Bangalore

This is valuable during MVP development because it lets the user test later phases even without external providers.

---

# 83. Manual Discovery Testing

Use manual companies to test:

    Company
      ↓
    Hiring Source Discovery
      ↓
    Job Discovery

This means we can build the core system without waiting for every external provider integration.

---

# 84. Acceptance Criteria

Phase 10.12 is complete only when:

- [ ] Canonical company records can be created.
- [ ] Company locations can be stored.
- [ ] Multiple locations per company are supported.
- [ ] Company normalization works.
- [ ] Website domains can be normalized.
- [ ] Conservative deduplication works.
- [ ] Discovery provider abstraction exists.
- [ ] User-provided company provider works.
- [ ] Discovery runs are recorded.
- [ ] Discovery status is tracked.
- [ ] Discovery confidence is stored.
- [ ] Provider failures are handled.
- [ ] Company search API works.
- [ ] Company detail API works.
- [ ] Discovery API works.
- [ ] Frontend discovery UI works.
- [ ] Candidate ownership is enforced for discovery runs.
- [ ] No unrestricted scraping is introduced.
- [ ] No job discovery is implemented.
- [ ] No hiring-source discovery is implemented.
- [ ] No matching is implemented.
- [ ] No AI-generated company facts are introduced.
- [ ] Backend tests pass.
- [ ] Frontend tests/build pass.
- [ ] Alembic migration passes.
- [ ] Existing functionality remains working.

---

# 85. Implementation Order

Implement sequentially:

1. Read this document.
2. Inspect current repository.
3. Inspect Phase 10.11 preferences implementation.
4. Inspect existing provider architecture.
5. Inspect database conventions.
6. Add Company model.
7. Add CompanyLocation model.
8. Add CompanyDiscoveryRun model.
9. Create Alembic migration.
10. Add provider abstraction.
11. Add UserProvidedCompanyProvider.
12. Add normalization logic.
13. Add conservative deduplication logic.
14. Add company repository.
15. Add discovery repository.
16. Add discovery service.
17. Add Pydantic schemas.
18. Add API endpoints.
19. Add frontend company service.
20. Add company discovery UI.
21. Add company detail UI.
22. Add backend tests.
23. Add provider tests.
24. Add deduplication tests.
25. Add API tests.
26. Add frontend tests/build.
27. Run migrations.
28. Run full test suite.
29. Inspect implementation.
30. Fix issues.
31. Verify architecture.
32. Produce final implementation report.

---

# 86. Codex Instructions

Implement ONLY Phase 10.12.

Before implementation:

- Inspect Phase 10.11.
- Inspect existing candidate preference models.
- Inspect existing provider architecture.
- Inspect existing database conventions.
- Inspect existing API conventions.
- Inspect existing authentication/ownership implementation.

Do not redesign previous phases.

Do not introduce:

- Google Maps scraping
- LinkedIn scraping
- Naukri scraping
- Indeed scraping
- Wellfound scraping
- browser automation
- Playwright
- Selenium
- paid APIs
- Redis
- Celery
- Kafka
- Qdrant
- Gemini
- RAG
- job matching

The MVP must work without an external paid company-data API.

Use a provider abstraction and a user-provided/manual provider.

Do not invent companies.

Do not invent company locations.

Do not claim companies are hiring.

Do not implement Phase 10.13 or later.

If an architectural contradiction exists, report it before making a major architectural change.

---

# 87. Final Implementation Report

After implementation provide:

## Implemented

Exact functionality.

## Database

List:

- companies
- company_locations
- company_discovery_runs
- optional run-result table
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

## APIs

List every endpoint.

## Frontend

Explain:

- discovery page
- company list
- company detail
- manual company creation
- discovery status

## Security

Explain:

- authentication
- candidate ownership
- provider credential handling

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

## Remaining

Confirm that:

- Phase 10.13 was NOT implemented.
- Phase 10.14 was NOT implemented.
- Job discovery was NOT implemented.
- Hiring-source discovery was NOT implemented.
Why 10.12 is a major milestone

This is where your original product idea starts becoming real.

Before this, we have:

Who am I?
    ↓
What can I do?
    ↓
Which roles do I want?
    ↓
Where do I want to work?

Now we add:

Where are the relevant companies?

So the eventual pipeline becomes:

Candidate
   ↓
Preferences
   ↓
HSR Layout / Bangalore
   ↓
Company Discovery
   ↓
Companies
   ↓
10.13 Hiring Source Discovery
   ↓
Where each company actually hires
   ↓
10.14 Job Discovery
   ↓
Actual current openings