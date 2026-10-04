mplementation specification for Codex

This phase is part of Phase 10 — MVP Implementation.

Important: Phase 10.14 already introduced job discovery and basic normalization needed to safely ingest a job. Phase 10.15 does not recreate the job domain. Instead, it makes normalization a dedicated, deterministic, reusable domain service.

10.14 = acquire and persist job listings.
10.15 = turn source job data into consistent canonical job data.

Do not implement Phase 10.16+ in this phase.

1. Objective

Build the Job Normalization layer that converts job listings collected from different sources into a consistent canonical representation.

The system may receive the same job from:

company career page
LinkedIn
Naukri
Indeed
Wellfound
another permitted provider
user-provided job data

Each source can represent the same information differently.

For example:

Frontend Engineer
Front-End Engineer
Frontend Developer
Software Engineer - Frontend
Frontend Engineer - Bangalore

The system must preserve the original source information while creating a consistent canonical representation.

The goal is:

Raw Source Job
      ↓
Source Adapter
      ↓
RawJobRecord
      ↓
Canonical Normalizer
      ↓
Normalized Job
      ↓
Identity / Deduplication
      ↓
Canonical Job
      ↓
PostgreSQL

This normalized job will later be consumed by:

10.16 JD Analysis
10.17 Candidate Matching
10.18 Resume Selection
10.19 Resume Tailoring
2. Phase Boundary

The distinction between 10.14 and 10.15 is important.

Phase 10.14 — Job Discovery

Responsible for:

Company
   ↓
Hiring Sources
   ↓
Discover listings
   ↓
Create job source records
   ↓
Store jobs

10.14 may perform minimal normalization required to safely persist a listing.

For example:

trim URL
extract title
identify company
store source metadata
Phase 10.15 — Job Normalization

Responsible for:

source job data
      ↓
consistent canonical representation
      ↓
field normalization
      ↓
identity resolution
      ↓
deduplication
      ↓
data quality validation
      ↓
canonical job

There must be one reusable normalization service rather than separate normalization logic inside every provider.

3. Goals

Implement:

deterministic job normalization
provider-independent normalization
canonical title normalization
location normalization
employment type normalization
seniority normalization
workplace mode normalization
experience range normalization
salary normalization
URL normalization
description cleanup
timestamp normalization
job status normalization
source provenance preservation
canonical job identity resolution
duplicate detection
idempotent normalization
normalization versioning
normalization status tracking
data quality validation
normalization tests
4. Non-Goals

Do not implement:

JD semantic analysis
candidate matching
skill extraction
AI-based normalization
Gemini calls
embeddings
Qdrant
RAG
resume generation
resume tailoring
candidate-job matching
application tracking
outreach
browser automation
unrestricted scraping
Google Maps scraping
LinkedIn scraping
Naukri scraping
job ranking

Those belong to later phases.

5. Core Principle

The normalization layer must be deterministic first.

Given the same input:

same source data
+
same normalization version

the result should be the same.

For example:

" Bengaluru "
"Bangalore"
"BENGALURU"

may normalize to:

Bengaluru

But the system must not use an LLM to decide this.

AI-based interpretation belongs to later JD analysis.

6. Existing Database Domain

Reuse the tables created in Phase 10.14.

Do not recreate:

jobs
job_sources
job_locations

Expected relationship:

Company
   │
   └── Job
         │
         ├── JobLocation
         │
         └── JobSource
                │
                └── CompanyHiringSource

A canonical job can have multiple source records.

Example:

Canonical Job
Frontend Engineer
Company: Example Technologies
Location: Bengaluru

       ├── Official Careers source
       ├── LinkedIn source
       └── Naukri source

The source records remain separate.

7. Source Data vs Canonical Data

This distinction is mandatory.

Source data

Represents what the provider gave us.

Example:

source_title:
"Frontend Engineer - Bangalore"

source_description:
"<div>We are looking for...</div>"

source_url:
"https://example.com/jobs/123"

source_metadata:
{
    "department": "Engineering",
    "location": "Bangalore",
    "workplace": "Hybrid"
}

This information must not be silently destroyed.

Canonical data

Represents the normalized application-level representation.

Example:

canonical_title:
Frontend Engineer

location:
Bengaluru

workplace_mode:
hybrid

department:
Engineering

The canonical representation can change as the normalization rules improve.

The source representation should remain available for provenance.

8. Normalization Pipeline

Implement this pipeline:

Job Source
    ↓
Load source record
    ↓
Validate source data
    ↓
Build RawJobRecord
    ↓
Normalize individual fields
    ↓
Build NormalizedJobRecord
    ↓
Validate normalized result
    ↓
Resolve canonical job identity
    ↓
Create/update canonical job
    ↓
Create/update job location
    ↓
Attach source record
    ↓
Update normalization metadata
9. Internal Data Contracts

Create internal Pydantic models.

Suggested location:

backend/app/schemas/jobs/

or the project's existing schema organization.

Create concepts equivalent to:

RawJobRecord
NormalizedJobRecord
NormalizedJobLocation
NormalizationResult
10. RawJobRecord

The raw internal representation should contain the source information required for normalization.

Example:

class RawJobRecord:
    job_source_id: UUID
    company_id: UUID

    source_title: str | None
    source_description: str | None

    source_url: str | None
    application_url: str | None
    external_job_id: str | None

    location: str | None

    employment_type: str | None
    seniority: str | None
    workplace_mode: str | None

    department: str | None

    experience_min: str | int | float | None
    experience_max: str | int | float | None

    salary_min: str | int | float | None
    salary_max: str | int | float | None
    salary_currency: str | None
    salary_period: str | None

    status: str | None

    first_seen_at: datetime | None
    last_seen_at: datetime | None

Adapt this to the actual existing model.

Do not duplicate fields unnecessarily if the current schema already provides them.

11. NormalizedJobRecord

The normalized representation should contain canonical values.

Example:

class NormalizedJobRecord:
    canonical_title: str
    normalized_title: str

    description: str | None

    employment_type: EmploymentType
    seniority: Seniority
    workplace_mode: WorkplaceMode

    department: str | None

    experience_min: float | None
    experience_max: float | None

    salary_min: float | None
    salary_max: float | None
    salary_currency: str | None
    salary_period: SalaryPeriod | None

    application_url: str | None
    status: JobStatus

    locations: list[NormalizedJobLocation]

    normalization_version: str
12. Canonical Title Normalization

Create deterministic title normalization.

Input examples:

" Frontend Engineer "
"FRONTEND ENGINEER"
"Frontend Engineer - Bangalore"
"Frontend Engineer | Bengaluru"
"Frontend Engineer (Hybrid)"

Normalization should:

trim whitespace
collapse repeated whitespace
normalize obvious formatting
remove meaningless surrounding punctuation
preserve meaningful title information
create a normalized comparison value

Example:

canonical_title:
Frontend Engineer

normalized_title:
frontend engineer
Important

Do not aggressively rewrite job titles.

For example:

"Senior Frontend Engineer - React"

must not automatically become:

Frontend Engineer

because:

Senior
React

may contain meaningful information.

If location is clearly a suffix, it may be removed from the canonical comparison title only when the rule is deterministic and safe.

When uncertain:

Preserve the original title.

13. Normalized Title

Maintain a comparison-friendly field.

Example:

canonical_title:
Frontend Engineer

normalized_title:
frontend engineer

Another:

canonical_title:
Senior Full Stack Engineer

normalized_title:
senior full stack engineer

The normalized value is for:

duplicate detection
search
comparison

It is not the display title.

14. Description Normalization

Source descriptions may contain HTML.

Example:

<div>
<h2>About the role</h2>
<p>We are looking for...</p>
</div>

Convert it into readable canonical text:

About the role

We are looking for...

Rules:

remove unsafe HTML
preserve meaningful text
decode HTML entities
normalize whitespace
preserve paragraphs where possible
remove navigation/footer noise when deterministic
do not summarize
do not rewrite meaning

The canonical jobs.description may contain cleaned text.

The original source description remains available through the source record.

15. Do Not Analyze the Description

This phase must not extract:

skills
requirements
responsibilities
qualifications
benefits
years of experience

from free-form text using AI.

For example:

"We are looking for someone with React and TypeScript..."

must remain description text.

Skill extraction belongs to:

Phase 10.16 — JD Analysis
16. Location Normalization

Normalize job locations into:

location_name
area
city
state
country
postal_code
latitude
longitude
location_type

Do not introduce PostGIS/geocoding in this phase.

Example:

Bangalore
Bengaluru
Bengaluru, Karnataka
Bangalore, Karnataka, India

should be normalized consistently where deterministic.

For example:

city:
Bengaluru

state:
Karnataka

country:
India
17. Area-Level Locations

The product is location-first.

Therefore preserve area-level information.

Example:

HSR Layout, Bengaluru

should not become only:

Bengaluru

Instead:

location_name:
HSR Layout

area:
HSR Layout

city:
Bengaluru

state:
Karnataka

country:
India

Do not throw away useful geographic specificity.

18. Workplace Mode

Normalize source values into:

remote
hybrid
onsite
flexible
unknown

Examples:

"Remote"
"100% remote"
"Work from home"

→

remote

Examples:

"Hybrid"
"2 days office / 3 days remote"

→

hybrid

Examples:

"On-site"
"Office based"

→

onsite

If the source does not provide enough evidence:

unknown

Never guess.

19. Employment Type

Normalize to the existing controlled values:

full_time
part_time
contract
internship
freelance
temporary
unknown

Examples:

Permanent
Full-time
Full Time

→

full_time

Examples:

Contract
Contractor

→

contract

If ambiguous:

unknown
20. Seniority

Normalize to:

intern
junior
mid
senior
lead
manager
director
unknown

Examples:

Junior Software Engineer

→

junior
Senior Frontend Engineer

→

senior
Engineering Manager

→

manager

Do not infer seniority solely from years of experience if the source explicitly provides another value.

21. Experience Range

Normalize source representations such as:

2-4 years
2 to 4 years
2+ years
Minimum 2 years
3 years experience

into:

experience_min
experience_max

Examples:

2-4 years

→

min = 2
max = 4
2+ years

→

min = 2
max = null
Minimum 3 years

→

min = 3
max = null

Do not invent an upper bound.

22. Salary Normalization

Normalize salary into:

salary_min
salary_max
salary_currency
salary_period

Examples:

₹8 LPA

→

salary_min = 800000
salary_max = 800000
currency = INR
period = annual

Example:

₹8-12 LPA

→

800000
1200000
INR
annual

Example:

$100k-$120k/year

→

100000
120000
USD
annual
Critical rule

If salary is not present:

salary_min = null
salary_max = null

Do not estimate.

Do not use market averages.

Do not ask Gemini.

23. Salary Period

Normalize to controlled values such as:

hourly
monthly
annual
unknown

If the provider says:

₹50,000/month

preserve:

50000
INR
monthly

Do not convert it to annual unless the schema explicitly requires conversion.

24. Currency Normalization

Normalize symbols and obvious codes.

Examples:

₹ → INR
Rs → INR
INR → INR

$ → USD
USD → USD

€ → EUR
EUR → EUR

Do not infer currency merely from a company location when salary information does not specify it.

25. URL Normalization

Normalize:

source_url
application_url

Rules:

trim whitespace
require valid URL format
normalize obvious formatting
remove unnecessary fragments where safe
preserve meaningful query parameters
do not blindly strip all query parameters
use HTTPS where the source explicitly provides HTTPS
do not follow redirects during basic normalization

Example:

https://example.com/job/123/

should consistently compare against equivalent forms where appropriate.

26. Job Status

Normalize source status into:

active
inactive
expired
unknown

Examples:

Open
Active
Hiring

→

active

Examples:

Closed
No longer accepting applications

→

inactive

If the provider does not provide status:

unknown

Do not mark a job active simply because it was discovered.

Discovery and freshness are separate concepts.

27. Timestamp Normalization

All timestamps stored in PostgreSQL should use the application's standard timezone strategy.

Prefer:

UTC

for persisted timestamps.

Normalize:

first_seen_at
last_seen_at
last_verified_at

Do not silently reinterpret ambiguous local timestamps.

28. Source Provenance

Every canonical job must remain traceable to its source records.

Example:

Job
 ├── JobSource A
 │     └── Official Careers
 │
 ├── JobSource B
 │     └── LinkedIn
 │
 └── JobSource C
       └── Naukri

Never merge jobs while losing source provenance.

29. Normalization Metadata

Extend the existing job_sources model if necessary.

Suggested fields:

normalization_status
normalization_version
normalization_error
normalized_at

Values:

pending
normalized
failed
needs_review

Example:

normalization_status = normalized
normalization_version = "1.0"
normalized_at = 2026-10-04T...

If the existing implementation already has equivalent fields, reuse them.

Do not create duplicate fields.

30. Job Normalization Version

Add or reuse:

jobs.normalization_version
jobs.normalized_at

if not already present.

Example:

normalization_version:
"1.0"

normalized_at:
2026-10-04T10:30:00Z

This allows future rules to change from:

1.0

to:

1.1

without losing track of which rules produced the canonical data.

31. Database Migration

Create an Alembic migration only for fields that do not already exist.

Potential additions:

job_sources.normalization_status
job_sources.normalization_version
job_sources.normalization_error
job_sources.normalized_at

jobs.normalization_version
jobs.normalized_at

Do not recreate existing:

jobs
job_sources
job_locations

tables.

Migration must be:

reversible
tested
consistent with existing SQLAlchemy models
32. Normalization Service

Create a dedicated service.

Suggested:

backend/app/services/job_normalization_service.py

Responsibilities:

load job source
→ construct RawJobRecord
→ normalize
→ validate
→ resolve canonical job
→ persist
→ update source status

Example conceptual API:

normalize_job_source(job_source_id)

Return:

NormalizationResult

containing:

job_id
job_source_id
status
normalization_version
created
updated
issues
33. Normalizer Module

Separate pure normalization logic from database operations.

Suggested:

backend/app/services/job_normalizer.py

or:

backend/app/normalization/jobs/
    normalizer.py
    titles.py
    locations.py
    salary.py
    experience.py
    urls.py

Follow the project's actual structure if an equivalent architecture already exists.

The important separation is:

Pure normalization
        ↓
Persistence

Do not mix every regex and database query into one huge function.

34. Field Normalizers

Create reusable deterministic functions for:

normalize_title()
normalize_location()
normalize_workplace_mode()
normalize_employment_type()
normalize_seniority()
normalize_experience()
normalize_salary()
normalize_url()
normalize_description()
normalize_status()

Each should be:

deterministic
independently testable
provider-agnostic
safe with null values
documented
35. Provider Independence

Do not write:

if provider == "linkedin":
    ...
elif provider == "naukri":
    ...

inside the core normalizer.

Provider-specific transformations belong in the provider adapter.

Architecture:

LinkedIn Provider
      ↓
RawJobRecord
      ↓
Common Normalizer
      ↓
Canonical Job

and:

Naukri Provider
      ↓
RawJobRecord
      ↓
Common Normalizer
      ↓
Canonical Job

This allows future providers without rewriting the core normalization engine.

36. Canonical Job Identity

The system must determine whether a source listing corresponds to an existing canonical job.

Use identity rules in this order.

Tier 1 — Provider + External Job ID
provider
+
external_job_id

Strongest source identity.

Tier 2 — Source URL

If the normalized source URL uniquely identifies the listing:

normalized_source_url

use it.

Tier 3 — Application URL

If appropriate:

company
+
normalized application URL
Tier 4 — Company + Title + Location

Use:

company_id
+
normalized_title
+
normalized location

as a conservative fallback.

37. Never Deduplicate by Title Alone

This is invalid:

Frontend Engineer

→ assume all jobs with this title are the same.

The same company may have:

Frontend Engineer — Bengaluru
Frontend Engineer — Mumbai
Frontend Engineer — Chennai

These are separate jobs.

38. Description Similarity

Do not implement AI/embedding-based similarity in this phase.

A future implementation may use:

description similarity

but that belongs to a later enhancement.

For MVP:

strong deterministic identifiers first

If identity cannot be established confidently:

create separate canonical job

rather than risk an incorrect merge.

39. Deduplication Principle

False merging is worse than temporary duplication.

Prefer:

two possible jobs

over incorrectly merging:

two different jobs

because incorrect merging can cause:

wrong applications
wrong job details
wrong matching
incorrect analytics
bad resume tailoring
40. Multiple Source Records

Suppose:

Official Careers:
Frontend Engineer
Bengaluru

LinkedIn:
Frontend Engineer
Bangalore

Naukri:
Frontend Engineer
Bengaluru

The system should create:

1 canonical job

with:

3 job_sources

not:

3 canonical jobs

when deterministic identity confirms they are the same opening.

41. Conflict Handling

Sources may disagree.

Example:

Official:
Hybrid

LinkedIn:
Remote

Do not silently replace one source with another.

For MVP:

Rule 1

Preserve source-level values.

Rule 2

Use the first trustworthy canonical value when available.

Rule 3

Only fill missing canonical values from later sources.

Rule 4

Do not overwrite populated canonical values merely because another source differs.

Rule 5

Future source-priority intelligence can improve this.

This avoids destructive data merging.

42. Source Confidence

Use existing source status/confidence information where available.

A source marked:

verified
high confidence
official careers

is stronger than:

unknown
low confidence
aggregator

But this phase should not build a complicated source-ranking engine.

Just avoid destructive overwrites.

43. Data Quality Validation

After normalization, validate required information.

Minimum acceptable canonical job:

company_id
canonical_title
source provenance

At least one of:

source_url
application_url
external_job_id

should normally exist.

If the job cannot satisfy minimum requirements:

normalization_status = failed

or:

needs_review

depending on the reason.

44. Partial Data Is Allowed

A job may legitimately have:

salary = null
experience = null
seniority = unknown

This is not automatically a failure.

Example:

Frontend Engineer
Bengaluru
Hybrid

Salary: unknown
Experience: unknown

is still a valid job.

Do not reject jobs merely because optional fields are absent.

45. Unknown vs Null

Use these deliberately.

Null

Means:

The information was not available.

Example:

salary_min = null
Unknown enum

Means:

The field exists conceptually, but the source did not allow us to determine its category.

Example:

workplace_mode = unknown

Do not convert everything into fake defaults.

46. Idempotency

Normalization must be safe to run multiple times.

Example:

normalize(job_source_id)
normalize(job_source_id)
normalize(job_source_id)

must not create:

3 jobs

It should maintain:

1 canonical job
1 source record

and update normalization metadata.

47. Re-Normalization

The system must support future normalization versions.

Example:

Job Source
normalization_version = 1.0

Later:

normalization_version = 1.1

A future migration/reprocessing task can identify:

all jobs where normalization_version < current_version

and normalize them again.

Do not build the full batch reprocessing system now.

48. API Design

The normalization engine is primarily an internal application service.

Do not expose unnecessary normalization endpoints.

If the existing architecture needs an explicit endpoint for manual/reprocessing operations, implement:

POST /api/v1/job-sources/{job_source_id}/normalize

Response:

{
  "job_id": "...",
  "job_source_id": "...",
  "status": "normalized",
  "normalization_version": "1.0"
}

Candidate ownership must still be respected where discovery records are candidate-scoped.

For shared canonical jobs, authorization must not accidentally allow arbitrary mutation.

49. Job Discovery Integration

Update Phase 10.14's discovery pipeline so that:

discover source job
      ↓
persist source record
      ↓
call JobNormalizationService
      ↓
canonical job

Do not duplicate normalization code inside discovery.

The correct architecture is:

JobDiscoveryService
        ↓
JobNormalizationService
        ↓
JobRepository
50. Error Handling

If normalization fails:

job_sources.normalization_status = failed
job_sources.normalization_error = safe error message

Do not:

crash the entire discovery run
expose stack traces to users
log secrets
lose the source record

The raw source record should remain available for debugging/retry.

51. Transaction Handling

Canonical job creation/update and source normalization state should be coordinated carefully.

Preferred flow:

Begin transaction

Load source
Normalize
Resolve canonical job
Create/update job
Create/update location
Update source normalization state

Commit

If the transaction fails:

rollback

and leave enough state for retry.

Avoid half-created canonical records.

52. Repository Layer

Use existing repository architecture.

Potential methods:

get_job_source()
find_job_by_external_identity()
find_job_by_source_url()
find_candidate_canonical_job()
create_job()
update_job()
create_job_location()
update_job_source_normalization_status()

Do not put large database queries inside the normalizer itself.

53. Indexes

Review existing indexes from 10.14.

Useful indexes include:

job_sources.external_job_id
job_sources.normalized_source_url
job_sources.job_id
job_sources.normalization_status

jobs.company_id
jobs.normalized_title
jobs.status

Do not add indexes blindly.

Only add indexes that support actual normalization queries.

54. Logging

Log normalization events using structured logging.

Example:

job_source_id
job_id
normalization_version
status
provider
duration_ms

Do not log:

authentication tokens
provider credentials
sensitive candidate information
entire job descriptions unnecessarily
55. Security

External job data is untrusted.

Treat:

job title
description
URLs
metadata
provider payloads

as untrusted input.

Never allow source data to:

execute HTML/JavaScript
inject SQL
alter authorization
control agent permissions
override system instructions later

This becomes especially important when JD content reaches the AI layer in Phase 10.16+.

56. No LLM

This phase must not call:

Gemini
OpenAI
Claude
local LLM

for normalization.

Do not add:

agent
prompt
LLM tool
RAG retrieval

to this phase.

Normalization must remain deterministic.

57. No Vector Database

Do not modify:

Qdrant
embeddings
vector collections

for this phase.

Semantic job understanding begins later.

58. Suggested Code Structure

Use the existing project architecture.

A possible structure:

backend/app/
├── services/
│   ├── job_discovery_service.py
│   ├── job_normalization_service.py
│   └── job_normalizer.py
│
├── repositories/
│   ├── job_repository.py
│   └── job_source_repository.py
│
├── schemas/
│   └── jobs/
│       ├── normalization.py
│       └── ...
│
├── utils/
│   └── normalization/
│       ├── text.py
│       ├── urls.py
│       ├── locations.py
│       ├── salary.py
│       └── experience.py
│
└── db/
    └── models/
        ├── job.py
        ├── job_source.py
        └── job_location.py

Do not blindly create every file above if the existing architecture already has equivalent locations.

Reuse the project's conventions.

59. Unit Tests

Test each normalizer independently.

Title
" Frontend Engineer "
→ "Frontend Engineer"
Location
"Bangalore, Karnataka"
→ Bengaluru, Karnataka
Employment
"Full Time"
→ full_time
Workplace
"Work From Home"
→ remote
Salary
"₹8-12 LPA"
→ 800000-1200000 INR annual
Experience
"2-4 years"
→ 2-4
URL

Test equivalent URL formats.

Description

Test:

HTML
whitespace
entities
empty description
60. Integration Tests

Test:

JobSource
   ↓
NormalizationService
   ↓
CanonicalJob
   ↓
JobLocation

Verify:

source preserved
canonical job created
normalization metadata saved
location created
repeated normalization is idempotent
61. Deduplication Tests

Test:

Same external ID
Source A external ID = 123
Source A external ID = 123

→ one canonical job.

Same source URL

→ one canonical job.

Different location
Frontend Engineer — Bengaluru
Frontend Engineer — Mumbai

→ two jobs.

Same title, different company

→ two jobs.

Same title alone

→ do not merge.

62. Conflict Tests

Example:

Source A:
Hybrid

Source B:
Remote

Verify:

source A still says hybrid
source B still says remote

and the canonical record is not destructively overwritten simply because another source disagrees.

63. Failure Tests

Test:

missing title
invalid source URL
missing company
malformed salary
malformed experience
invalid enum
malformed timestamps
database failure
duplicate source
normalization retry

The source record should remain recoverable.

64. Authorization Tests

Verify:

unauthenticated requests rejected
candidate cannot access another candidate's private discovery data
shared canonical job access follows intended authorization
source records cannot be modified by an unrelated candidate
browser-supplied candidate IDs are not trusted for identity

Continue using Firebase authentication from Phase 10.4.

65. Frontend

Phase 10.15 does not require a large new UI.

Existing job discovery/detail UI from 10.14 should display normalized values.

For example:

Frontend Engineer
Example Technologies

Bengaluru
Hybrid
Full-time
2–4 years
₹8–12 LPA

Do not display an artificial:

100% normalized

or similar meaningless score.

Optionally show source information:

Found via Official Careers
Also found via LinkedIn

but do not create a complex normalization dashboard.

66. Example End-to-End

Input:

Title:
" Senior Front-End Engineer - Bangalore "

Location:
"Bangalore, Karnataka"

Type:
"Full Time"

Workplace:
"Hybrid"

Experience:
"3-5 years"

Salary:
"₹10-15 LPA"

Description:
"<p>We are looking for a frontend engineer...</p>"

URL:
"https://example.com/jobs/123"

Normalized:

canonical_title:
Senior Front-End Engineer

normalized_title:
senior front end engineer

city:
Bengaluru

state:
Karnataka

country:
India

employment_type:
full_time

workplace_mode:
hybrid

experience_min:
3

experience_max:
5

salary_min:
1000000

salary_max:
1500000

salary_currency:
INR

salary_period:
annual

status:
active

The source values remain preserved.

67. Example With Missing Data

Input:

Title:
Frontend Engineer

Location:
Bengaluru

Type:
Full-time

Salary:
not provided

Output:

canonical_title:
Frontend Engineer

city:
Bengaluru

employment_type:
full_time

salary_min:
null

salary_max:
null

salary_currency:
null

salary_period:
unknown

This is valid.

68. Example With Ambiguous Data

Input:

Title:
Engineer

Location:
India

Workplace:
Flexible

Salary:
Competitive

Output may be:

canonical_title:
Engineer

workplace_mode:
flexible

salary_min:
null

salary_max:
null

salary_currency:
null

salary_period:
unknown

Do not invent salary.

69. Acceptance Criteria

Phase 10.15 is complete only when:

 Existing 10.14 job tables are reused.
 Dedicated normalization service exists.
 Pure deterministic normalizers exist.
 Source data is preserved.
 Canonical data is generated consistently.
 Titles are normalized.
 Locations are normalized.
 Workplace modes are normalized.
 Employment types are normalized.
 Seniority is normalized.
 Experience is normalized.
 Salary is normalized.
 URLs are normalized.
 Descriptions are safely cleaned.
 Status is normalized.
 Source provenance is preserved.
 Duplicate detection is deterministic.
 Same source job is idempotent.
 Multiple sources can point to one canonical job.
 Different jobs are not aggressively merged.
 Normalization version is tracked.
 Failed normalization can be retried.
 Discovery uses the centralized normalization service.
 Unit tests pass.
 Integration tests pass.
 Authorization tests pass.
 Existing 10.1–10.14 functionality still works.
 No AI/LLM/RAG/vector implementation is introduced.