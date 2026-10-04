# Phase 10.11 — Candidate Preferences

## 1. Purpose

Phase 10.11 introduces the candidate's job-search preferences.

The system needs to understand not only:

> "What can this candidate do?"

but also:

> "What kind of opportunities does this candidate actually want?"

This distinction is critical for the job discovery system.

For example, a candidate may be technically qualified for:

- Frontend Engineer
- Full Stack Engineer
- Backend Engineer
- Forward Deployed Engineer

but may only want:

- Bangalore
- Mumbai
- Chennai
- Pune
- Hyderabad

and may prefer:

- Hybrid
- On-site
- Remote

with certain salary expectations and company preferences.

The preference system becomes an input to later:

- Company Discovery
- Hiring Source Discovery
- Job Discovery
- Job Filtering
- Matching
- Recommendations
- Career Assistant

---

# 2. Core Principle

Preferences describe what the candidate wants.

They do NOT describe what the candidate is capable of.

Therefore:

Candidate Profile
    ↓
"What I am / what I have done"

Role Profile
    ↓
"What roles I want to position myself for"

Preferences
    ↓
"What opportunities I want"

Example:

Candidate Profile:
    Angular
    TypeScript
    Python
    FastAPI
    AWS

Role Profiles:
    Frontend Engineer
    Full Stack Engineer
    Forward Deployed Engineer

Preferences:
    Locations:
        Bangalore
        Mumbai
        Chennai
        Pune
        Hyderabad

    Work Mode:
        On-site
        Hybrid

    Employment:
        Full-time

These are separate concepts and must remain separate in the database.

---

# 3. Why Preferences Are Important

The product's core differentiation is not simply:

> "Find software jobs."

The system should eventually support:

> "Find companies and relevant jobs around the locations I actually want."

Therefore the agent needs structured preferences.

Example request:

"Find frontend and full-stack opportunities around HSR Layout."

The system should be able to combine:

```text
Candidate
+
Role Profile
+
Location Preferences
+
Work Preferences
+
Job Preferences

before discovering and ranking opportunities.

4. Scope

Phase 10.11 includes:

Candidate preference model
Location preferences
Target role preferences
Work-mode preferences
Employment-type preferences
Experience/seniority preferences
Salary preferences
Company preferences
Job-search preferences
Remote preference
Active/inactive preference state where needed
Preference CRUD APIs
Frontend preference UI
Validation
Candidate ownership
Tests
5. Explicitly NOT Included

Do NOT implement:

Company discovery
Location intelligence
Google Maps integration
Job discovery
LinkedIn scraping
Naukri scraping
Indeed scraping
Wellfound scraping
Job matching
JD analysis
Resume tailoring
Applications
Agent orchestration
RAG
Qdrant
Automatic recommendations
Automatic job searches

This phase only stores and manages candidate preferences.

6. Relationship With Previous Phases

The current architecture is:

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

Preferences become one of the major inputs to discovery.

7. Preference Architecture

Use a normalized model where appropriate.

Recommended high-level relationship:

Candidate
|
+---- CandidatePreference
|
+---- PreferenceLocation
|
+---- PreferenceRole
|
+---- PreferenceCompanyCriteria

However, do not create unnecessary tables for values that can safely be represented as controlled fields.

The implementation should follow the existing project conventions.

8. Candidate Preferences

Recommended table:

candidate_preferences
--------------------------------
id
candidate_id
employment_type
min_experience_years
max_experience_years
min_salary
max_salary
salary_currency
salary_period
remote_preference
relocation_preference
company_size_preference
company_stage_preference
job_search_active
created_at
updated_at

Because preferences may evolve, fields should remain flexible enough for later additions.

9. One-to-One Relationship

For MVP:

Candidate
    |
    +---- CandidatePreference

Each candidate has one main preference record.

Use:

candidate_id UNIQUE

so the database enforces one preference record per candidate.

10. Employment Type

Recommended controlled values:

full_time
part_time
contract
internship
freelance
temporary

A candidate may want multiple employment types.

Therefore, do NOT force the main table into a single value if the product needs multiple selections.

Preferred normalized structure:

candidate_preference_employment_types
--------------------------------------
id
candidate_preference_id
employment_type

with:

UNIQUE(candidate_preference_id, employment_type)

For the initial MVP, full_time should be sufficient as a default if that matches the product requirement.

Do not silently assume all candidates want full-time employment.

11. Work Mode

Controlled values:

remote
hybrid
onsite

A candidate may select more than one.

Example:

Work mode:
    Hybrid
    On-site

This means:

I am open to both.

It does NOT mean:

The job must be hybrid.

The matching system later determines how strongly the job matches the preference.

12. Remote Preference

Avoid redundant fields such as:

remote = true
work_mode = hybrid

if they can conflict.

Prefer one canonical representation:

work_modes:
    remote
    hybrid
    onsite

This avoids contradictory state.

13. Location Preferences

Location is a major product feature.

The system must support:

City
State/region
Country
Neighborhood/area
Remote
Relocation willingness
Search radius later

Example:

Bangalore
Mumbai
Chennai
Pune
Hyderabad

Do not store only free-form text if the location will later be used for discovery.

14. Location Preference Table

Recommended:

candidate_preference_locations
--------------------------------
id
candidate_preference_id
location_name
city
state
country
location_type
priority
is_primary
created_at

Possible location_type:

city
area
region
country

For MVP:

city
area

are sufficient.

15. Example

Candidate preference:

Bangalore
Mumbai
Chennai
Pune
Hyderabad

could be represented as:

location_name    city        state       priority
--------------------------------------------------
Bangalore        Bangalore   Karnataka   1
Mumbai           Mumbai      Maharashtra 2
Chennai          Chennai     Tamil Nadu  3
Pune             Pune        Maharashtra 4
Hyderabad        Hyderabad   Telangana   5

The priority allows the candidate to say:

Bangalore is my first choice.

without preventing discovery elsewhere.

16. Area-Level Location

The product must eventually support:

HSR Layout
Koramangala
Whitefield
Indiranagar
Electronic City

This is important for the company's location-first discovery strategy.

However, Phase 10.11 should not implement geographic intelligence.

Store the candidate's requested area.

Later Phase 10.12 can resolve:

HSR Layout
    ↓
Bangalore
    ↓
coordinates / geographic boundary

using an approved provider.

17. Do Not Geocode Yet

Do NOT introduce:

Google Maps
Mapbox
OpenStreetMap API
geocoding APIs
PostGIS

in Phase 10.11.

Store normalized location information only.

Geographic resolution belongs to Company Discovery / Location Intelligence.

18. Primary Location

A candidate may mark one location as primary.

Example:

Bangalore      primary
Mumbai         secondary
Chennai        secondary

This can later influence search ordering.

Database/application must ensure only one primary preference location.

19. Target Role Preferences

Role Profiles already exist.

Therefore, do NOT duplicate role names inside preferences unless necessary.

The candidate can select:

Preferred Role Profiles
    ↓
Frontend Engineer
Full Stack Engineer
Forward Deployed Engineer

This relationship should reference:

role_profiles.id

rather than copying the designation text.

Recommended:

candidate_preference_role_profiles
-----------------------------------
id
candidate_preference_id
role_profile_id
priority
is_primary
created_at

This creates:

Candidate Preference
↓
Role Profile
↓
Verified Candidate Data

20. Why Role Preferences Reference Role Profiles

Suppose the candidate changes:

Frontend Engineer

to:

Frontend / UI Engineer

The preference should still reference the same role profile.

Avoid:

preferred_role = "Frontend Engineer"

as a free-form string when a canonical role profile already exists.

21. Target Seniority

Candidate preferences may include target seniority.

Example:

junior
mid
senior
lead

A candidate may select multiple levels.

For example:

junior
mid

The system should not automatically decide seniority solely from years of experience.

22. Experience Range

Optional:

min_experience_years
max_experience_years

Example:

minimum: 0
maximum: 3

This means the candidate is open to roles requiring approximately that range.

This is a search preference, not proof of actual experience.

The candidate's actual experience remains in the candidate profile.

23. Salary Preferences

Support:

min_salary
max_salary
salary_currency
salary_period

Example:

min_salary: 600000
max_salary: 1000000
currency: INR
period: yearly

Do not hard-code INR into the database.

The application may default the UI to INR for the user's region, but the database should remain currency-aware.

24. Salary Period

Controlled values:

yearly
monthly
hourly

For normal full-time software jobs, yearly is expected to be most common.

Still keep the model extensible.

25. Salary Is a Preference, Not a Hard Filter

Suppose:

candidate max = ₹10 LPA
job salary = ₹11 LPA

The system should not necessarily eliminate the job.

Salary data may be:

missing
inaccurate
a range
base only
total compensation
estimated

Therefore later matching should distinguish:

salary match
salary unknown
salary exceeds preference

Do not hard-code this logic into Phase 10.11.

26. Company Preferences

The candidate may eventually want:

Startup
Mid-size
Enterprise
Product companies
Service companies
Early-stage startups
Growth-stage companies

Recommended controlled fields:

company_size_preference
company_stage_preference

However, these should be optional.

Do not force candidates to classify companies.

27. Company Size

Possible controlled values:

startup
small
medium
large
enterprise

These values are intentionally broad.

Later Company Intelligence can map actual employee counts into these categories.

28. Company Stage

Possible values:

pre_seed
seed
series_a
series_b
series_c_plus
public
unknown

Do not require this field for MVP.

29. Company Preference Philosophy

Do not make the preference model overly restrictive.

For example:

company_stage = startup

should mean:

Prefer startups.

It should not automatically mean:

Reject every company whose stage is unknown.

Later matching can use:

preferred
acceptable
unknown

rather than only true/false.

30. Job Search Active

Add:

job_search_active

This tells the system whether the candidate is currently looking.

Example:

true

When false:

automated discovery should not run
notifications should be paused
scheduled searches should not run

This becomes important later when automation is introduced.

31. Relocation Preference

Recommended controlled values:

not_willing
open
required

Meaning:

not_willing

Candidate does not want relocation.

open

Candidate may relocate for the right opportunity.

required

Candidate specifically wants opportunities requiring relocation.

For MVP, not_willing and open are enough if simpler implementation is desired.

32. Location + Relocation Example

Candidate:

Preferred cities:
Bangalore
Mumbai

Relocation:
Open

Later discovery may include:

Pune
Hyderabad

but the system should distinguish:

preferred location

from:

relocation-compatible location
33. Preference Priority

Preferences are not all equal.

Example:

Role:
    Full Stack Engineer       priority 1
    Frontend Engineer         priority 2
    FDE                       priority 3

Location:
    Bangalore                 priority 1
    Mumbai                    priority 2
    Pune                      priority 3

Store priority where it is useful.

Do not over-normalize every scalar field.

34. Preference APIs

Recommended:

GET /api/v1/preferences
PUT /api/v1/preferences

Since preferences are one-to-one with candidate, a separate POST is not necessary if:

PUT

creates or updates the resource.

This makes the operation idempotent.

35. Location APIs

Recommended:

GET    /api/v1/preferences/locations
POST   /api/v1/preferences/locations
PUT    /api/v1/preferences/locations/{location_id}
DELETE /api/v1/preferences/locations/{location_id}
POST   /api/v1/preferences/locations/{location_id}/set-primary
36. Role Preference APIs

Recommended:

GET    /api/v1/preferences/roles
POST   /api/v1/preferences/roles
DELETE /api/v1/preferences/roles/{role_profile_id}
POST   /api/v1/preferences/roles/{role_profile_id}/set-primary

The relationship should use the authenticated candidate's role profile.

37. Employment Type APIs

If employment types are stored in a relationship table:

GET    /api/v1/preferences/employment-types
POST   /api/v1/preferences/employment-types
DELETE /api/v1/preferences/employment-types/{employment_type}

Alternatively, the main preference PUT endpoint may update the complete list.

Use whichever style is consistent with the existing API architecture.

Do not create unnecessary endpoints.

38. Example Preference Response
{
  "id": "uuid",
  "job_search_active": true,
  "work_modes": [
    "hybrid",
    "onsite"
  ],
  "employment_types": [
    "full_time"
  ],
  "target_seniority": [
    "junior",
    "mid"
  ],
  "min_experience_years": 0,
  "max_experience_years": 3,
  "min_salary": 600000,
  "max_salary": 1000000,
  "salary_currency": "INR",
  "salary_period": "yearly",
  "relocation_preference": "open",
  "locations": [],
  "role_profiles": []
}

The exact representation should follow the actual implemented schema.

39. Candidate Ownership

All preference data must be scoped to the authenticated candidate.

Never accept:

candidate_id

from the frontend as an authorization mechanism.

Use:

Firebase Token
    ↓
Verified UID
    ↓
Candidate
    ↓
Preferences
40. Location Ownership

Candidate A must not be able to modify:

Candidate B's location preference

Test this explicitly.

41. Role Profile Ownership

Candidate A must not be able to attach:

Candidate B's role profile

to Candidate A's preferences.

The backend must validate:

role_profile.candidate_id == authenticated_candidate.id
42. Preference Validation

Validate:

Salary
min_salary >= 0
max_salary >= min_salary
Experience
min_experience >= 0
max_experience >= min_experience
Priority
priority >= 1
Controlled enums

Reject unsupported values.

43. Location Validation

Do not attempt to verify whether a location is geographically real in this phase.

For example:

HSR Layout

may be stored as:

location_type = area
city = Bangalore
state = Karnataka
country = India

Later location intelligence can verify/normalize it.

44. Location Normalization

Store a normalized form.

Example:

display_name:
HSR Layout

normalized_name:
hsr layout

Do not use normalized values as the user-facing display.

45. Duplicate Locations

Prevent duplicate preference locations.

For example:

Bangalore
Bangalore
Bangalore

should not create three records.

Use an appropriate uniqueness strategy based on:

candidate_preference_id
+
normalized location
46. Work Mode Selection UI

Example:

Work Mode

☑ Hybrid
☑ On-site
☐ Remote

This means:

accepted modes = hybrid + onsite
47. Location UI

Example:

Preferred Locations

1. Bangalore       Primary
2. Mumbai
3. Chennai
4. Pune
5. Hyderabad

[+ Add location]

The candidate should be able to reorder locations.

48. Role Preference UI

Example:

Target Roles

1. Full Stack Engineer     Primary
2. Frontend Engineer
3. Forward Deployed Engineer

[+ Add role profile]

Only existing role profiles should be selectable.

49. Salary UI

Example:

Expected Salary

Minimum: ₹ ______
Maximum: ₹ ______

Currency: INR
Period: Yearly

Do not require salary if the candidate does not want to specify it.

50. Job Search Toggle

Example:

Actively looking for jobs

[ ON ]

This will later control:

automated discovery
notifications
scheduled searches
recommendation generation

Do not implement those automations yet.

51. Preferences Page

Recommended layout:

Job Search Preferences

--------------------------------

Target Roles
[ Full Stack Engineer ]
[ Frontend Engineer ]
[ FDE ]

Preferred Locations
[ Bangalore ]
[ Mumbai ]
[ Chennai ]
[ Pune ]
[ Hyderabad ]

Work Mode
[✓] Hybrid
[✓] On-site
[ ] Remote

Employment
[✓] Full-time

Seniority
[✓] Junior
[✓] Mid

Salary
Minimum: ₹______
Maximum: ₹______

Relocation
[ Open to relocation ]

Company Preferences
[ Startup ]
[ Product ]
[ Enterprise ]

[Save Preferences]
52. Do Not Overcomplicate the UI

The candidate should not need to fill 30 fields before using the application.

The MVP should allow:

Target roles
+
Locations
+
Work mode
+
Employment type

at minimum.

Everything else can remain optional.

53. Default Values

Avoid silently choosing preferences that the candidate did not provide.

Safe defaults:

job_search_active = false

or whatever onboarding explicitly establishes.

Do not automatically assume:

remote = true

or:

salary = 0

or:

relocation = open

unless the product explicitly defines that behavior.

54. Preferences Are Not Hard Filters

This is a major architecture rule.

Suppose:

Preferred location:
Bangalore

Job location:
Pune

The system should later be able to explain:

Location:
Partial / outside primary preference

rather than simply throwing the job away.

This allows the candidate to discover unexpected opportunities.

55. Preference Matching Later

The future matching architecture can evaluate:

Role Match
Location Match
Work Mode Match
Employment Match
Salary Match
Seniority Match
Company Preference Match

Each can have its own evidence/status.

Example:

Role:       Strong
Location:   Strong
Work Mode:  Strong
Salary:     Unknown
Seniority:  Partial

This is better than one opaque number.

56. Product Philosophy

The system should distinguish:

Candidate Capability

from:

Candidate Preference

Example:

Candidate can work with:

AWS
Docker
FastAPI
Angular

but prefers:

Frontend
Full Stack
FDE

and wants:

Bangalore
Mumbai
Hybrid

A job may therefore be:

Technically suitable
+
Preference mismatch

or:

Technically partial
+
Preference excellent

The system should preserve both dimensions.

57. Future Company Discovery

Phase 10.12 will eventually use:

Candidate Preferences
       ↓
Preferred Locations
       ↓
Company Discovery
       ↓
Companies around requested areas

Example:

HSR Layout
   ↓
Companies in/around HSR
   ↓
Company websites
   ↓
Career pages
   ↓
Hiring sources

This is why area-level preferences are important now.

58. Future Job Discovery

Later:

Role Profiles
+
Preferences
+
Company Intelligence
+
Hiring Sources
        ↓
Job Discovery

The job discovery agent should not independently invent the candidate's preferences.

It should retrieve them from the canonical preference domain.

59. Agent Boundary

Do not add agents in Phase 10.11.

The future Career Orchestrator will retrieve:

Candidate Profile
Role Profiles
Preferences

through controlled tools.

For example:

get_candidate_preferences()
get_active_role_profiles()
get_preferred_locations()

Those tools belong to the later agent phase.

60. Database Integrity

Recommended relationships:

candidate_preferences.candidate_id
    → candidates.id

candidate_preference_locations.candidate_preference_id
    → candidate_preferences.id

candidate_preference_role_profiles.candidate_preference_id
    → candidate_preferences.id

candidate_preference_role_profiles.role_profile_id
    → role_profiles.id

Use foreign keys and appropriate cascade behavior.

61. Database Constraints

Recommended:

candidate_preferences.candidate_id UNIQUE

candidate_preference_locations
    UNIQUE(candidate_preference_id, normalized_location)

candidate_preference_role_profiles
    UNIQUE(candidate_preference_id, role_profile_id)

For employment/work-mode controlled values, use either:

application validation
PostgreSQL enum/check constraints

consistent with the existing database strategy.

62. Migration

Create an Alembic migration.

Do not modify previous migrations.

The migration should create the preference tables and indexes.

After migration:

alembic upgrade head

must succeed from an empty database.

63. Backend Structure

Possible additions:

backend/app/
├── api/
│   └── v1/
│       └── preferences.py
│
├── repositories/
│   └── preference_repository.py
│
├── schemas/
│   └── preference.py
│
└── services/
    └── preference_service.py

If the existing architecture uses separate repositories/services for sub-resources, follow that pattern.

Do not blindly create files if existing modules already provide the correct location.

64. Service Responsibilities

preference_service.py should handle:

Get candidate preferences
Create/update preference record
Add/remove locations
Add/remove role profiles
Update work modes
Update employment types
Validate ranges
Validate ownership
Set primary location
Set primary role
Maintain consistent state

It should not perform company/job discovery.

65. Repository Responsibilities

Repository handles:

CRUD
Relationship queries
Location queries
Role preference queries
Employment preference queries
Primary preference updates

It should not:

verify Firebase tokens
call external APIs
call Gemini
discover companies
discover jobs
66. Schema Responsibilities

Pydantic schemas should validate API input.

Examples:

CandidatePreferenceUpdate
CandidatePreferenceResponse

PreferenceLocationCreate
PreferenceLocationResponse

PreferenceRoleCreate
PreferenceRoleResponse

Use typed enums for controlled values where appropriate.

67. Frontend Service

Add something similar to:

preference.service.ts

Responsibilities:

Get preferences
Save preferences
Add location
Remove location
Update location
Add role profile
Remove role profile
Update preference selections

The frontend should not implement ownership logic.

68. Frontend State

After saving preferences, the UI should reflect the backend response.

Do not maintain a separate permanent source of truth in localStorage.

Local state can be used for UI state.

The database remains authoritative.

69. Security Tests

At minimum test:

Unauthenticated request
    → 401

Candidate A reads Candidate B preferences
    → denied

Candidate A modifies Candidate B location
    → denied

Candidate A attaches Candidate B role profile
    → denied
70. Validation Tests

Test:

negative salary
max salary < min salary
negative experience
max experience < min experience
invalid work mode
invalid employment type
duplicate location
duplicate role profile
invalid role profile ownership

All should behave according to the API contract.

71. Default/Primary Tests

Test:

Location A = primary
Location B = primary

Expected:

Location A = not primary
Location B = primary

Likewise for preferred role profiles.

72. Full Integration Test

Test:

Create Candidate
       ↓
Create Candidate Profile
       ↓
Create Role Profile
       ↓
Create Preferences
       ↓
Add Role Profile to Preferences
       ↓
Add Bangalore location
       ↓
Add Mumbai location
       ↓
Set Bangalore primary
       ↓
Save
       ↓
Retrieve

Verify the complete response.

73. Existing Functionality

After Phase 10.11 implementation, verify:

Authentication
Candidate onboarding
Candidate profile
Skills
Resume upload
Resume parsing
Role profiles

still work.

Do not accept regressions.

74. Acceptance Criteria

Phase 10.11 is complete when:

 Candidate preferences can be created.
 Candidate preferences can be updated.
 Candidate preferences can be retrieved.
 Candidate can select target role profiles.
 Candidate can add/remove preferred locations.
 Candidate can set primary location.
 Candidate can select work modes.
 Candidate can select employment types.
 Candidate can select target seniority.
 Candidate can optionally define experience range.
 Candidate can optionally define salary range.
 Candidate can define relocation preference.
 Candidate can optionally define company preferences.
 Candidate can enable/disable active job search.
 Duplicate relationships are prevented.
 Invalid values are rejected.
 Candidate ownership is enforced.
 Cross-candidate role profiles cannot be attached.
 No job discovery is implemented.
 No company discovery is implemented.
 No matching is implemented.
 Backend tests pass.
 Frontend tests/build pass.
 Alembic migration passes.
 Existing functionality remains working.
75. Implementation Order

Implement sequentially:

Read this document.
Inspect current repository.
Inspect Candidate model.
Inspect Candidate Profile implementation.
Inspect Skills implementation.
Inspect Role Profiles implementation.
Add preference database models.
Add preference relationship models.
Create Alembic migration.
Add repositories.
Add schemas.
Add service layer.
Add API routes.
Implement ownership checks.
Implement validation.
Implement primary location behavior.
Implement primary role behavior.
Implement frontend service.
Implement preferences page.
Add backend tests.
Add frontend tests.
Run migrations.
Run full test suite.
Run Angular production build.
Inspect implementation.
Fix issues.
Verify architecture.
Produce final implementation report.
76. Codex Instructions

Implement ONLY Phase 10.11.

Before changing code:

Inspect the actual Phase 10.10 implementation.
Inspect the actual candidate model.
Inspect the actual role-profile model.
Inspect the actual API conventions.
Inspect the actual authentication/ownership implementation.
Inspect existing migrations.

Do not recreate existing entities.

Do not replace existing architecture.

Do not introduce:

Google Maps
Mapbox
geocoding APIs
PostGIS
Redis
Celery
Kafka
Gemini
Qdrant
job providers
company providers
scraping

Do not implement Phase 10.12 or later.

If an architectural contradiction exists between the current repository and this specification, report it before making a major redesign.

77. Final Implementation Report

After implementation provide:

Implemented

Exact functionality.

Database

List:

tables
fields
foreign keys
indexes
unique constraints
migrations
APIs

List all endpoints.

Frontend

Explain:

preferences page
role selection
location management
work mode
employment type
salary
seniority
relocation
job-search toggle
Security

Explain:

Firebase authentication
candidate ownership
role-profile ownership
location ownership
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

Confirm: