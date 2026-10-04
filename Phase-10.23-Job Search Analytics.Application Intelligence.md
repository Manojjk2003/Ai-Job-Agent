Phase 10.23 — Job Search Analytics / Application Intelligence
# Phase 10.23 — Job Search Analytics / Application Intelligence

## 1. Purpose

Phase 10.23 introduces analytics and intelligence over the candidate's job-search activity.

The Career Agent should not only help the candidate:

- discover companies
- discover jobs
- match jobs
- prepare resumes
- apply
- contact recruiters
- track communication

It should also answer:

> "What is happening with my job search?"

and:

> "What should I improve based on the evidence?"

Examples:

- How many jobs did I discover this month?
- How many did I apply to?
- Which companies responded?
- Which resume/profile performs better?
- Which roles have the highest response rate?
- Am I applying mostly to jobs where I am a strong match?
- Are recruiters responding to outreach?
- Which locations are producing more opportunities?
- Which skills repeatedly appear in jobs I want?
- Where are applications getting stuck?
- Are rejections concentrated around particular requirements?
- Should I change my search strategy?

The goal is not to create meaningless dashboards.

The goal is:

> Job-search activity → measurable outcomes → evidence → actionable recommendations

---

# 2. Architectural Position

The existing flow becomes:

Candidate
    ↓
Profile
    ↓
Role Profiles
    ↓
Preferences
    ↓
Company Discovery
    ↓
Hiring Source Discovery
    ↓
Job Discovery
    ↓
JD Analysis
    ↓
Candidate Matching
    ↓
Resume Selection
    ↓
Resume Tailoring
    ↓
Application
    ↓
Outreach
    ↓
Communication
    ↓
Outcome
    ↓
Analytics / Intelligence
    ↓
Recommendations

Analytics is a consumer of existing domain data.

It should NOT become the source of truth for:

- jobs
- applications
- resumes
- candidate profile
- contacts
- outreach
- communications

---

# 3. Core Principle

Analytics must be derived from existing source-of-truth data.

Do not manually maintain counters such as:

```text
total_applications = 52

inside the candidate record.

Instead calculate:

COUNT(applications)

from application records.

Similarly:

response_rate

should be derived from application/outreach/communication events.

This prevents stale counters.

4. Scope

Implement:

Job-search activity analytics
Application funnel analytics
Application outcome analytics
Match-quality analytics
Resume analytics
Outreach analytics
Communication analytics
Company analytics
Location analytics
Hiring-source analytics
Skill-demand analytics
Search effectiveness analytics
Time-based trends
Candidate-facing dashboard
Recommendation engine
Analytics APIs
Tests
Privacy/security controls
5. Explicit Non-Goals

Do NOT implement:

external market-wide salary analytics
public labor-market statistics
predictive hiring guarantees
"you will get this job" predictions
automated resume changes
automatic profile changes
automatic application strategy changes
autonomous job applications
autonomous outreach
mass email
external scraping specifically for analytics
competitor intelligence
employer surveillance
analytics on other candidates
selling candidate analytics
training AI on candidate analytics without explicit product decision

Analytics should describe evidence from the candidate's own job-search activity.

6. Analytics Data Sources

The analytics layer may consume:

Candidate
candidate
candidate_profile
candidate_preferences
Skills
candidate_skills
skill_evidence
Role positioning
role_profiles
role_profile_skills
role_profile_experiences
role_profile_projects
Companies
companies
company_locations
company_hiring_sources
Jobs
jobs
job_sources
job_locations
job_skills
job_requirements
Matching
job_matches
match_evidence
Resumes
resumes
resume_versions
tailored_resumes
resume_claims
Applications
applications
application_events
Contacts / Outreach
contacts
outreach
outreach_events
Communication
email_threads
email_messages
communication_events
7. Analytics Categories

The dashboard should be divided into meaningful areas.

A. Search Activity

Measures:

companies discovered
jobs discovered
jobs viewed
jobs saved
jobs matched
jobs applied to
B. Application Funnel

Measures:

Discovered
   ↓
Viewed
   ↓
Matched
   ↓
Selected
   ↓
Tailored
   ↓
Prepared
   ↓
Applied
   ↓
Recruiter Contact
   ↓
Interview
   ↓
Offer

Not every stage must exist for every application.

C. Outcome

Measures:

applications
responses
interviews
offers
rejections
withdrawals
open applications
D. Match Quality

Measures:

strong matches
partial matches
weak matches
missing-skill patterns
preference conflicts
eligibility concerns
E. Resume Performance

Measures:

which base resume was selected
which role profile was used
tailored resume usage
application outcomes by resume/profile combination
F. Outreach

Measures:

outreach sent
recruiter replies
response rate
outreach-to-interview rate
G. Communication

Measures:

recruiter communications
interview invitations
assessments
rejections
offers
H. Search Strategy

Measures:

location performance
role performance
company performance
source performance
seniority performance
work-mode performance
I. Skill Intelligence

Measures:

frequently requested skills
missing skills
recurring requirements
candidate skill coverage
8. Time Windows

Analytics APIs should support time windows.

Suggested:

7d
30d
90d
6m
1y
all
custom

Do not hard-code only one time range.

Example:

GET /api/v1/analytics/overview?period=30d
9. Timezone

Analytics should respect candidate timezone where possible.

Do not blindly assume UTC for candidate-facing date boundaries.

Store timestamps consistently, preferably UTC.

Convert to candidate-local timezone for presentation.

10. Application Funnel

Create a funnel based on real events.

Example:

Jobs discovered       500
        ↓
Jobs viewed           120
        ↓
Strong/partial match   80
        ↓
Applications           35
        ↓
Responses              10
        ↓
Interviews              5
        ↓
Offers                  1

Do not claim that every discovered job was actually viewed unless the application records such an event.

11. Application Metrics

Useful metrics:

total_applications
active_applications
submitted_applications
rejected_applications
withdrawn_applications
interviewing_applications
offers
accepted_offers

Derived from application statuses and events.

12. Response Rate

A response should be defined carefully.

Example:

response_rate =
applications_with_recruiter_or_company_response
/
applications_with_sufficient_follow_up_window

Do not simply calculate:

responses / total applications

because very recent applications may not have had time to receive a response.

Example:

Application submitted yesterday

should not necessarily count as a failed/no-response application.

13. Follow-Up Window

Define a configurable observation window.

Example:

response_window_days = 14

The exact value should remain configurable.

Example:

Applications older than 14 days
        ↓
Eligible for response-rate calculation

New applications:

Still awaiting observation
14. Interview Rate

Possible definition:

interview_rate =
applications_reaching_interview
/
eligible_applications

Clearly label the denominator.

Do not present:

Interview rate: 50%

without explaining what it means.

Prefer:

5 interviews
out of
35 eligible applications
= 14.3%
15. Offer Rate

Possible:

offer_rate =
offers
/
eligible_applications

Also expose:

offers / interviews

when meaningful.

16. Outreach Analytics

Track:

outreach_sent
outreach_replied
outreach_failed
outreach_bounced
outreach_cancelled

Possible:

outreach_response_rate =
replied / eligible_sent

Possible:

outreach_to_interview_rate =
interviews_with_outreach
/
eligible_outreach

Always expose sample size.

17. Resume Analytics

The system should answer:

"Which resume/profile combination is producing better outcomes?"

Example:

Frontend Engineer Profile
    Applications: 18
    Recruiter responses: 5
    Interviews: 3

Full Stack Engineer Profile
    Applications: 20
    Recruiter responses: 2
    Interviews: 1

Do not conclude:

"Frontend resume is objectively better."

Instead say:

"Based on your current tracked applications, the Frontend Engineer profile has a higher observed response/interview rate."

Small sample sizes must be clearly indicated.

18. Role Analytics

Group applications by:

role_profile
target_designation
normalized job title

Example:

Frontend Engineer
Full Stack Engineer
Forward Deployed Engineer
Software Engineer

This is particularly important because the product is NOT restricted to a single title.

19. Location Analytics

Group opportunities/applications by:

area
city
state
country
remote
hybrid
onsite

Example:

HSR Layout
Koramangala
Whitefield
Bangalore
Mumbai
Pune
Remote

Do not require PostGIS for this phase.

Use normalized stored location fields.

20. Company Analytics

Show:

companies_discovered
companies_applied_to
companies_with_responses
companies_with_interviews
companies_with_offers

Potential view:

Company              Apps   Responses   Interviews
---------------------------------------------------
Company A              5        2           1
Company B              3        1           1
Company C              4        0           0

Do not expose private information about company employees.

21. Hiring Source Analytics

Compare sources such as:

official_careers
LinkedIn
Naukri
Indeed
Wellfound
user_provided
other_permitted_sources

Only include sources actually represented in the stored application/job data.

Example:

Source       Applications   Responses
--------------------------------------
Official          12           4
LinkedIn           8           1
Wellfound          5           2

Do not infer that a source is "bad" from a tiny sample.

22. Skill Demand Analytics

Use normalized job_skills.

Example:

Skill            Jobs   Required   Candidate Has
------------------------------------------------
TypeScript         42      30           Yes
React              38      28           Yes
AWS                35      24           Yes
Docker             27      18           Yes
Kubernetes         21      15           No

This provides useful learning intelligence.

23. Missing Skill Patterns

Identify recurring missing skills from jobs the candidate is interested in.

Example:

You analyzed 47 relevant jobs.

Frequently missing skills:

1. Kubernetes       18 jobs
2. Redis            13 jobs
3. GraphQL           9 jobs
4. Terraform         8 jobs

This is evidence from the candidate's tracked jobs, not a universal market ranking.

24. Skill Gap Recommendations

The system may recommend:

"Consider learning Kubernetes because it appears as a requirement
in 18 of the 47 jobs you analyzed."

But it must NOT say:

"Learn Kubernetes and you will get a job."

The recommendation is evidence-based, not a guarantee.

25. Match Quality Analytics

Use Phase 10.17 match categories:

strong_match
partial_match
missing
unknown

Example:

Strong match:
24

Partial:
18

Weak:
8

Compare application outcomes by match category.

Example:

Strong match applications:
20
Responses:
7

Partial match applications:
15
Responses:
2

This may reveal:

"Your strongest-match applications currently have a higher response rate."

Do not imply causation.

26. Match-to-Outcome Analysis

Possible relationship:

Match quality
      ↓
Application
      ↓
Response
      ↓
Interview

This can answer:

"Am I applying too broadly?"

Example recommendation:

Your last 30 eligible applications show a higher response rate
for strong matches than partial matches.

Consider prioritizing strong/partial matches before lower-confidence
applications.

This is a recommendation, not an automatic rule.

27. Application Quality Signals

Potential signals:

match category
role alignment
required skill coverage
preference alignment
resume selected
tailored resume used
outreach used
company source
location
seniority

Do not create a single magical "application quality score."

If a composite score is introduced later, its components must be transparent.

28. Resume Tailoring Analytics

Measure:

applications_using_base_resume
applications_using_tailored_resume
interviews_from_tailored_resume

Example:

Tailored resume:
24 applications
5 interviews

Base resume:
11 applications
1 interview

Again:

observed correlation ≠ proof of causation.

29. Search Strategy Intelligence

The system should identify patterns such as:

Most productive target role:
Frontend Engineer

Most productive location:
HSR / Bangalore

Highest observed response source:
Official company career pages

Highest observed response profile:
Frontend Engineer role profile

Only make recommendations when sample size is reasonable.

30. Minimum Sample Size

Avoid misleading recommendations from tiny samples.

Example:

1 application
1 interview
100% interview rate

This is technically true but statistically weak.

Display:

Sample size: 1

and avoid strong conclusions.

Possible confidence labels:

insufficient_data
early_signal
moderate_signal
stronger_signal

These labels describe evidence strength, not statistical certainty.

31. Recommendation Engine

Create a recommendation layer.

Suggested:

backend/app/services/analytics/
├── analytics_service.py
├── funnel_service.py
├── outcome_service.py
├── skill_demand_service.py
├── resume_analytics_service.py
├── outreach_analytics_service.py
└── recommendation_service.py

Recommendations should be generated from analytics facts.

Example:

Fact:
12 applications to frontend roles.

Fact:
5 recruiter responses.

Fact:
2 responses from tailored resumes.

Recommendation:
Continue prioritizing frontend roles and track whether the pattern
continues with additional applications.
32. Recommendation Structure

Suggested:

recommendations
----------------
id
candidate_id
type
title
description
evidence
priority
confidence
status
created_at
updated_at

Types:

search_strategy
role_strategy
resume_strategy
skill_learning
outreach_strategy
location_strategy
application_strategy

Status:

new
viewed
dismissed
accepted
expired
33. Recommendation Evidence

Every recommendation should explain why it exists.

Example:

{
  "recommendation": "Prioritize stronger matches",
  "evidence": {
    "strong_match_applications": 20,
    "strong_match_responses": 7,
    "partial_match_applications": 15,
    "partial_match_responses": 2
  }
}

Do not create unexplained recommendations.

34. Analytics API

Suggested:

GET /api/v1/analytics/overview

GET /api/v1/analytics/funnel

GET /api/v1/analytics/applications

GET /api/v1/analytics/outreach

GET /api/v1/analytics/communications

GET /api/v1/analytics/matches

GET /api/v1/analytics/resumes

GET /api/v1/analytics/roles

GET /api/v1/analytics/locations

GET /api/v1/analytics/companies

GET /api/v1/analytics/sources

GET /api/v1/analytics/skills

GET /api/v1/analytics/recommendations

POST /api/v1/analytics/recommendations/{id}/dismiss

All endpoints must derive data for the authenticated candidate.

35. Overview Response

Conceptual response:

{
  "period": "30d",
  "applications": {
    "total": 35,
    "active": 20,
    "rejected": 10,
    "interviewing": 4,
    "offers": 1
  },
  "responses": {
    "count": 10,
    "rate": 0.2857
  },
  "interviews": {
    "count": 5,
    "rate": 0.1428
  },
  "offers": {
    "count": 1
  }
}

The backend should clearly define how each number is calculated.

36. Analytics Query Layer

Avoid putting large analytics queries directly inside API routes.

Use:

API
 ↓
Analytics Service
 ↓
Analytics Repository / Query Layer
 ↓
PostgreSQL

Example:

analytics_service.get_application_funnel()

The route should not contain large SQL statements.

37. Performance

Analytics may eventually query large amounts of data.

For MVP:

use indexed PostgreSQL queries
avoid loading every record into Python
aggregate in SQL where practical
paginate detailed tables
cache only when necessary

Do not introduce Redis solely for analytics in this phase.

38. Database Indexing

Review indexes on:

applications(candidate_id)
applications(candidate_id, created_at)
application_events(application_id, event_at)

job_matches(candidate_id, job_id)
job_matches(candidate_id, created_at)

outreach(candidate_id, created_at)
outreach_events(outreach_id, event_at)

email_messages(candidate_id, received_at)
communication_events(candidate_id, event_at)

jobs(company_id)
jobs(created_at)
job_locations(city)
job_locations(area)

Only add indexes justified by actual query patterns.

39. Analytics Snapshots

Do NOT create precomputed analytics tables unless necessary.

For MVP:

Source tables
    ↓
SQL aggregation
    ↓
Analytics response

Later, if scale requires it:

Source tables
    ↓
Aggregation jobs
    ↓
Analytics snapshots

Do not prematurely build a data warehouse.

40. Frontend Dashboard

Create an analytics dashboard.

Suggested:

Dashboard
├── Overview
├── Application Funnel
├── Outcomes
├── Match Quality
├── Resume Performance
├── Outreach
├── Communication
├── Roles
├── Locations
├── Companies
├── Hiring Sources
├── Skills
└── Recommendations
41. Overview UI

Example:

Job Search Overview
---------------------------------

Last 30 days

Applications          35
Responses             10
Interviews             5
Offers                 1

Response Rate       28.6%
Interview Rate       14.3%

---------------------------------

Application Funnel

Discovered     500
Matched         80
Applied         35
Responses       10
Interviews       5
Offers           1
42. Recommendations UI

Example:

What the system is learning

┌─────────────────────────────────────┐
│ Prioritize strong matches           │
│                                     │
│ Your strong-match applications      │
│ currently receive more responses    │
│ than partial-match applications.    │
│                                     │
│ Evidence: 20 applications           │
│ Strong-match responses: 7           │
│                                     │
│ [View evidence] [Dismiss]           │
└─────────────────────────────────────┘
43. Skill Intelligence UI

Example:

Skills appearing frequently in your jobs

Kubernetes       18 jobs
Redis            13 jobs
GraphQL           9 jobs
Terraform         8 jobs

Your current profile:
Kubernetes       Missing
Redis            Partial
GraphQL          Missing
Terraform        Missing

Do not automatically add skills to the candidate profile.

44. Candidate Control

Analytics should never silently modify:

candidate profile
candidate skills
preferences
role profiles
resumes
applications
outreach

Recommendations may suggest changes.

Candidate remains in control.

45. AI Usage

AI is optional.

Do NOT use AI for basic arithmetic.

For example:

35 applications
10 responses

should be calculated deterministically.

AI may be used for:

summarizing trends
explaining patterns
generating natural-language recommendations
identifying semantic patterns in qualitative evidence

But AI should receive structured analytics facts rather than raw database access.

Example:

Analytics facts
      ↓
Gemini
      ↓
Structured recommendation
46. AI Provider Abstraction

Use the existing LLM provider abstraction.

Do not call Gemini directly from:

analytics_service.py

Use:

AnalyticsInsightProvider

or the existing general LLM abstraction if appropriate.

Example:

class AnalyticsInsightProvider:
    def generate_insight(self, analytics_context):
        ...

Gemini can be the first implementation.

47. AI Input Restrictions

The AI should receive:

aggregated metrics
match statistics
skill statistics
resume statistics
application outcomes

Do not send unnecessary:

email bodies
phone numbers
private contact information
OAuth tokens
passwords
unrelated personal data

Email content should only be included if a specific communication-analysis feature requires it.

48. AI Output Validation

Use Pydantic structured output.

Example:

class AnalyticsRecommendation(BaseModel):
    title: str
    description: str
    recommendation_type: str
    confidence: str
    evidence: list[dict]

Validate output before persistence.

Reject unsupported recommendation types.

49. Recommendation Safety

AI must not generate claims such as:

"You will get this job."

"This company definitely rejects candidates without Kubernetes."

"LinkedIn is useless."

"Your resume guarantees interviews."

Allowed:

"Among your tracked applications, jobs requiring Kubernetes
have produced fewer matches."

The recommendation must be grounded in the candidate's own data.

50. Privacy

Analytics data belongs to the candidate.

Every analytics query must enforce:

authenticated candidate
+
candidate-owned records

No cross-candidate aggregation in the MVP.

Do not expose:

another candidate's application data
another candidate's communication
another candidate's response rates
another candidate's resume performance
51. Auditability

For important AI-generated recommendations, retain enough information to explain the recommendation.

Store:

recommendation
evidence
generation method
model/provider
generation version
created_at

Do not store unnecessary raw sensitive data.

52. Recommendation Versioning

Recommendations may become stale.

Example:

Recommendation created:
October 4

New applications:
October 20

Old recommendation:
Potentially stale

Recommendations should either:

be regenerated
be marked stale
have an expiration time

Do not keep presenting old recommendations as current truth.

53. Analytics Events

Do not invent fake user activity.

Only record real events.

Examples:

JOB_VIEWED
JOB_SAVED
JOB_MATCHED
RESUME_SELECTED
RESUME_TAILORED
APPLICATION_PREPARED
APPLICATION_SUBMITTED
OUTREACH_SENT
OUTREACH_REPLIED
INTERVIEW_RECEIVED
APPLICATION_REJECTED
OFFER_RECEIVED

If the product currently lacks some event, add it only where the corresponding user/system action actually exists.

54. Event Consistency

Prefer existing:

application_events
outreach_events
communication_events

rather than creating a giant generic event table unnecessarily.

Analytics should consume domain events.

55. Data Quality

Analytics should identify insufficient data.

Example:

You have only 3 tracked applications.

Analytics are still early.

Do not display highly confident recommendations from tiny datasets.

56. Empty States

Examples:

No applications yet.

Start applying to jobs and your application analytics
will appear here.

For skills:

Not enough analyzed jobs yet.

Continue discovering jobs to see recurring skill demand.
57. Error Handling

If analytics calculation fails:

Do not return partially fabricated numbers.

Return a controlled error.

Example:

{
  "error": "analytics_unavailable"
}

Log the internal error securely.

Do not expose SQL details.

58. Testing

Implement:

Authentication
unauthenticated analytics request rejected
authenticated candidate sees only own analytics
Application Analytics
total applications
active applications
rejected applications
interview count
offer count
Funnel
correct stage counts
duplicate events do not inflate metrics
recent applications handled correctly
Response Rate
eligible application calculation
observation window
recent applications excluded appropriately
Resume Analytics
correct resume grouping
correct role-profile grouping
small sample handling
Outreach
sent count
reply count
response rate
Skills
job skill frequency
candidate skill comparison
missing skill frequency
Location
city aggregation
area aggregation
remote/hybrid/onsite
Recommendations
evidence included
stale recommendations handled
unsupported AI output rejected
Security
candidate isolation
no cross-candidate analytics
sensitive communication data not exposed unnecessarily
59. Acceptance Criteria

Phase 10.23 is complete when:

Analytics
candidate can view job-search metrics
metrics are derived from real application/job/outreach/communication data
time ranges work
empty states work
Funnel
candidate can see application funnel
funnel numbers are reproducible from source data
Outcomes
responses
interviews
offers
rejections
active applications

are represented accurately.

Matching
match-quality analytics exist
strong/partial/missing patterns can be viewed
Resume
resume/profile performance can be compared
sample sizes are visible
Outreach
outreach response analytics exist
Skills
recurring job skills can be identified
candidate skill coverage can be compared
Search Strategy
role
location
company
hiring source

can be analyzed where sufficient data exists.

Recommendations
recommendations are evidence-based
evidence is visible
AI is optional and constrained
no automatic profile/application changes occur
Security
Firebase authentication enforced
candidate ownership enforced
no cross-candidate analytics
Testing
backend tests pass
frontend tests/build pass
analytics queries are verified
recommendation validation is tested
60. Important Architectural Rules

Codex MUST:

Inspect all existing Phase 10.20–10.22 implementations before coding.
Reuse existing domain tables.
Do not recreate applications.
Do not recreate outreach.
Do not recreate communications.
Do not create duplicate event systems unnecessarily.
PostgreSQL remains the source of truth.
Analytics are derived from source-of-truth data.
Candidate ownership must be enforced.
Do not expose other candidates' analytics.
Do not use AI for deterministic arithmetic.
Do not invent analytics data.
Do not create unsupported conclusions.
Show evidence behind recommendations.
Handle small sample sizes explicitly.
Keep analytics provider-agnostic.
Keep Gemini behind the existing provider abstraction.
Do not introduce Redis/data warehouse prematurely.
Do not introduce microservices.
Do not redesign the approved architecture.
Do not implement Phase 10.24+.
61. Implementation Order

Implement sequentially:

Step 1

Inspect existing:

applications
application events
outreach
outreach events
communications
job matching
resumes
role profiles
skills
Step 2

Identify available event/data sources.

Step 3

Implement analytics repository/query layer.

Step 4

Implement application funnel analytics.

Step 5

Implement application outcome analytics.

Step 6

Implement match-quality analytics.

Step 7

Implement resume/profile analytics.

Step 8

Implement outreach/communication analytics.

Step 9

Implement role/location/company/source analytics.

Step 10

Implement skill-demand analytics.

Step 11

Implement recommendation model/service.

Step 12

Implement deterministic recommendations.

Step 13

Add optional AI-generated insights.

Step 14

Add analytics APIs.

Step 15

Implement Angular dashboard.

Step 16

Add tests.

Step 17

Run:

Python compile
backend tests
migration checks
Angular tests
Angular production build
Step 18

Inspect dashboard manually.

Step 19

Verify calculations against raw database records.

Step 20

Fix issues.

Step 21

Verify architecture against Phase 0–9.

62. Final Codex Report

At the end provide:

Implementation Summary

What was implemented.

Analytics

All analytics implemented.

Metrics

Definitions/formulas used.

APIs

All endpoints.

Database

Tables added/modified.

Recommendations

How recommendations are generated.

AI

Whether AI was implemented and where.

Frontend

Dashboard/components/pages.

Security

Candidate isolation and privacy controls.

Tests

Exact test results.

Build

Backend/frontend results.

Warnings

All warnings.

Errors

All errors and fixes.

Architectural Decisions

Important decisions.

Deviations

Any deviations from this specification.

If a major architectural contradiction is found:

STOP before making the change and explain:

What contradicts.
Why it matters.
Current architecture.
Proposed change.
Impact.

Do not silently redesign.

End of Phase 10.23

### What you're learning here

This phase teaches an important real-world engineering concept: **analytics should sit on top of your transactional system, not become a second source of truth.**

Your architecture is now becoming:

```text
                  ┌── Resume
                  ├── Application
Candidate ────────┼── Outreach
                  ├── Communication
                  ├── Matching
                  └── Jobs
                         │
                         ▼
                  Analytics Layer
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Dashboard              Recommendations