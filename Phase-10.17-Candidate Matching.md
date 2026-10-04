1. Objective

Build an explainable Candidate ↔ Job Matching system.

The system should answer:

How well does this candidate fit this particular job, and why?

It must not simply produce:

87% Match

Instead, it should produce structured evidence such as:

Required skills
────────────────────────────
React          → Strong match
TypeScript     → Strong match
Python         → Partial match
PostgreSQL     → Missing

Preferred skills
────────────────────────────
AWS            → Strong match
Docker         → Strong match

Experience
────────────────────────────
Job requires: 2+ years
Candidate: 1.5 years
→ Partial / eligibility concern

Overall:
Strong technical alignment
Some experience gap

The system must explain how it reached every important conclusion.

2. Phase Boundary

The pipeline is now:

10.14 Job Discovery
        ↓
10.15 Job Normalization
        ↓
10.16 JD Analysis
        ↓
10.17 Candidate Matching
        ↓
10.18 Resume Selection
        ↓
10.19 Resume Tailoring
10.16

Extracts:

Job requires:
React
TypeScript
Python
2+ years
AWS preferred
10.17

Compares that against:

Candidate:
React
TypeScript
1.5 years
AWS
10.18

Will later determine:

Which existing resume/profile should be used?

10.19

Will later create:

A truthful job-specific tailored resume.

3. Core Product Principle

The system must never invent candidate capability.

The candidate is the source of truth for:

candidate_skills
experiences
projects
education
certifications
resume evidence

The job is the source of truth for:

job_requirements
job_skills
experience requirements
education requirements
certifications

Matching is a comparison layer.

Candidate Truth
       +
Job Requirements
       ↓
Matching Evidence
4. What Matching Is NOT

Do not build a generic ATS score.

Do not claim:

"ATS score = 91"

unless there is a very explicit, documented scoring methodology.

Even then, the product should emphasize:

strong match
partial match
missing
eligibility concern
unknown

rather than pretending the system can know how an external ATS ranks the candidate.

5. Matching Categories

Use the following primary statuses:

strong_match
partial_match
missing
not_applicable
unknown

For eligibility-related requirements, also support:

meets
concern
unknown

The exact implementation can use separate dimensions rather than forcing everything into one enum.

6. Matching Dimensions

At minimum evaluate:

Skills
Experience
Education
Certifications
Role alignment
Location/work mode
Employment type
Seniority

Not every dimension needs to produce a positive/negative result.

Example:

Salary
→ preference, not candidate capability

should not automatically become a candidate failure.

7. Matching Architecture

Use:

Candidate
   │
   ├── Candidate Profile
   ├── Candidate Skills
   ├── Experiences
   ├── Projects
   ├── Education
   ├── Certifications
   └── Role Profiles
            │
            ▼
       Matching Service
            ▲
            │
   ┌────────┴────────┐
   │                 │
Job Skills      Job Requirements
   │                 │
   └────────┬────────┘
            ▼
      Match Evidence
            │
            ▼
       Job Match
8. Database Design

Use the approved global architecture:

job_match
match_evidence

If these tables do not yet exist, implement them in this phase.

Do not create candidate-specific copies of jobs or JDs.

9. Job Match

Create:

job_matches

Suggested fields:

id
candidate_id
job_id
status
match_version
analysis_version
candidate_profile_version
overall_category
overall_score
confidence
created_at
updated_at

Important:

overall_score is optional and must never replace the evidence.

If implemented, it must be clearly defined as an internal product score, not an ATS score.

10. Match Uniqueness

A candidate should normally have one active/current match result per job for a given matching version.

Conceptually:

candidate_id
+
job_id
+
match_version

should prevent accidental duplicate active results.

Historical versions may remain.

11. Match Evidence

Create:

match_evidence

Suggested fields:

id
job_match_id
requirement_id
job_skill_id
candidate_skill_id
candidate_experience_id
candidate_project_id
evidence_type
match_status
importance
candidate_evidence
job_evidence
reason
confidence
created_at
updated_at

Not every foreign key needs to be populated.

The important principle is:

Every significant matching conclusion should be traceable to evidence.

12. Example Match Evidence

Job:

React required

Candidate:

React
Candidate skill
Intermediate

Evidence:

Job:
"Strong React experience required."

Candidate:
"React used in Teacher Progress Tracking project."

Result:
strong_match

This is much more useful than:

React = 0.91 similarity
13. Candidate Evidence Sources

Candidate capability can come from:

candidate_skills
experiences
experience_achievements
projects
project_skills
education
certifications
resume_versions
role_profiles

Use the actual entities implemented in previous phases.

Do not assume every candidate claim is equally strong.

14. Evidence Strength

A candidate may say:

React

but the system may also have:

React
↓
Project
↓
Implementation evidence

The second is stronger evidence.

Potential evidence types:

verified_experience
project
education
certification
resume
candidate_claim

Use the existing skill_evidence model from Phase 10.7 where applicable.

15. Skill Matching

This is the most important matching dimension.

Example:

Job:
React
TypeScript
Python
PostgreSQL
Docker

Candidate:
React
TypeScript
FastAPI
MySQL
Docker

Result:

React       → strong_match
TypeScript  → strong_match
Python      → partial_match / related
PostgreSQL  → partial_match / related
Docker      → strong_match

Do not automatically treat:

FastAPI = Python
MySQL = PostgreSQL

as exact skill matches.

16. Skill Relationship Categories

Use:

exact
alias
strongly_related
related
missing
unknown

Example:

Job: ReactJS
Candidate: React
→ alias/exact

Job: Python
Candidate: FastAPI
→ related, but Python should still be checked

Job: PostgreSQL
Candidate: MySQL
→ related database technology, not exact

This prevents false positives.

17. Skill Alias Matching

Reuse Phase 10.7:

skills
skill_aliases

Example:

React.js
ReactJS
React

should resolve to:

React

before matching.

18. Skill Matching Must Not Be Name-Only

Do not simply do:

candidate_skill.name in job_skill.name

Use canonical skill IDs wherever possible.

Pipeline:

Job skill
   ↓
Canonical Skill
   ↓
Candidate canonical Skills
   ↓
Relationship evaluation
19. Skill Evidence

For each important skill match store:

job_skill
candidate_skill
match_status
relationship
reason
evidence

Example:

React
────────────────────────
Status: Strong match

Job:
"3+ years React experience."

Candidate:
React listed as a candidate skill.
React used in SLH project.

Reason:
Candidate has the requested skill and project evidence.
20. Proficiency

Candidate skills may contain:

beginner
intermediate
advanced
expert

Use this information carefully.

Example:

Job:
Advanced React expertise

Candidate:
Beginner React

should not become:

strong_match

It may be:

partial_match

or:

concern

depending on the explicit job requirement.

21. Years of Experience

Candidate skill may have:

years_experience

Job may require:

minimum years

Example:

Job:
React ≥ 2 years

Candidate:
React = 3 years

Result:
strong_match

Example:

Job:
React ≥ 3 years

Candidate:
React = 1 year

Result:
partial_match

If candidate years are unknown:

unknown

Do not infer years from job title alone.

22. Experience Matching

Compare:

Job minimum experience
Candidate verified/declared experience

Example:

Job:
2+ years

Candidate:
2.5 years

→ meets

Example:

Job:
5+ years

Candidate:
2 years

→ concern
23. Candidate Experience Calculation

Do not blindly calculate total career duration from every database row if the model contains:

internships
education projects
part-time work
overlapping jobs

Use the candidate's verified years_experience where available.

If the system calculates experience from experience records, document the calculation rules.

Do not double-count overlapping periods.

24. Experience Evidence

Example:

Job:
"3+ years of backend development."

Candidate:
2.4 years professional backend experience.

Result:
partial_match / concern

Evidence:
Candidate experience records:
2024-2026 Backend Developer
25. Responsibilities Are Not Hard Requirements

Example:

Job responsibility:
"Collaborate with frontend developers."

The candidate should not automatically fail if they have no explicit:

collaboration skill

Responsibilities are useful for role alignment, but should not be treated as mandatory requirements unless the JD explicitly frames them as requirements.

26. Education Matching

Example:

Job:
Bachelor's degree in Computer Science or related field.

Candidate:
BCA Computer Applications.

The system should be careful.

It may determine:

related degree

but this is a semantic judgment.

Use structured education information plus AI only where needed.

Do not claim:

guaranteed eligible

if the employer's definition is unclear.

Preferred output:

Likely meets

or:

Potential eligibility concern

with explanation.

27. Certification Matching

Example:

Job:
AWS Certified Solutions Architect required.

Candidate:
No AWS certification found.

Result:
missing

If:

Job:
AWS certification preferred.

Candidate:
No certification.

Result:

preferred requirement missing

This should not have the same impact as a missing mandatory certification.

28. Seniority Matching

Compare:

Job seniority
Candidate target seniority
Candidate experience

Example:

Job:
Junior

Candidate:
Junior

→ aligned

Example:

Job:
Senior

Candidate:
Junior

→

seniority concern

Do not reject automatically.

A candidate may still choose to apply.

29. Role Alignment

Candidate may have role profiles:

Frontend Engineer
Full Stack Engineer
Forward Deployed Engineer

Job:

Software Engineer - Frontend

This may align with:

Frontend Engineer

The matching system should consider role profiles.

Do not require exact job title equality.

30. Role Profile Evidence

Example:

Candidate Role Profile:
Frontend Engineer

Target designation:
Frontend Developer

Primary skills:
Angular
TypeScript
React

Job:

Frontend Engineer

→ strong role alignment.

31. Location Matching

Candidate preferences may contain:

HSR Layout
Bengaluru

Job location:

Koramangala
Bengaluru

The system should distinguish:

candidate preference

from:

candidate capability

Location fit is an opportunity preference, not a skill.

32. Location Categories

Use:

preferred
acceptable
concern
unknown

Example:

Candidate:
Bengaluru preferred

Job:
Bengaluru

→ preferred location match

Example:

Candidate:
Bengaluru only

Job:
Mumbai onsite

→ location concern

Do not block the job unless the product's preference rules explicitly define it as a hard filter.

33. Remote/Hybrid Matching

Candidate preferences:

hybrid
onsite
remote

Job:

hybrid

Result:

aligned

Candidate:

remote only

Job:

onsite

Result:

work-mode concern

Again, preference ≠ capability.

34. Employment Type

Compare:

candidate preferences

with:

job employment_type

Example:

Candidate:
full_time

Job:
full_time

→ aligned

Example:

Candidate:
full_time only

Job:
internship

→ preference mismatch
35. Salary

Do not treat salary as a capability match.

Instead use it as:

preference alignment

Example:

Candidate:
minimum ₹8 LPA

Job:
₹10–12 LPA

→ salary preference aligned

If job salary is unavailable:

unknown

Do not assume it is below the candidate's expectation.

36. Missing Data

Missing information must not automatically mean failure.

Example:

Job:
AWS required

Candidate:
AWS not listed

This may be:

missing

But if the candidate has not fully completed their profile:

unknown

may be more appropriate.

The system must distinguish:

"I don't have evidence"

from:

"I know the candidate does not have it."

This is a major design principle.

37. Candidate Profile Completeness

Consider adding:

profile completeness

to matching context.

Example:

Candidate profile:
40% complete

Then a missing skill should have lower confidence.

Do not automatically downgrade all matches mathematically; simply preserve confidence.

38. Match Confidence

Every match conclusion can have:

high
medium
low

Example:

Candidate explicitly lists React
+ project evidence
→ high confidence

Candidate only has:

"Frontend development"

while job requires:

React

→ lower confidence.

39. Explainable Overall Result

Instead of:

87%

produce a summary:

Overall:
Strong alignment

Strong matches:
7

Partial matches:
2

Missing required:
1

Preference concerns:
1

Eligibility concerns:
0

This is much more actionable.

40. Optional Internal Score

If an overall numerical score is implemented, it must be:

deterministic
documented
reproducible
based on explicit weights
not called an ATS score

Example conceptual weighting:

Required skills       50%
Experience            20%
Role alignment        10%
Education             5%
Certifications        5%
Preferences           10%

But do not blindly adopt these numbers.

The implementation should first establish an explicit scoring model.

If there is no strong need for a numerical score in MVP:

Prefer no score.

Use categories and evidence.

41. Recommendation

The system may generate:

strongly_consider
consider
consider_with_gaps
low_alignment
insufficient_data

These are product recommendations, not employment predictions.

Example:

Strong technical alignment.
One required skill is missing.
Worth applying if the candidate can demonstrate equivalent experience.

Do not say:

You will get the job.
42. Match Engine Architecture

Create:

backend/app/services/matching_service.py

Conceptually:

MatchingService
      │
      ├── SkillMatcher
      ├── ExperienceMatcher
      ├── EducationMatcher
      ├── CertificationMatcher
      ├── RoleMatcher
      └── PreferenceMatcher

Do not make one giant function.

43. Matching Should Be Mostly Deterministic

Core comparisons should be deterministic.

For example:

canonical skill ID
candidate skill ID

does not require an LLM.

Use AI only where semantic interpretation is genuinely required.

This makes the system:

cheaper
faster
reproducible
testable
explainable
44. Optional AI Semantic Layer

Some relationships may require semantic interpretation.

Example:

Job:
"Experience building RESTful backend services."

Candidate:
"Developed FastAPI APIs."

These may be related.

If an LLM is used:

MatchingService
      ↓
SemanticMatcher
      ↓
LLM Provider

The LLM must return structured evidence.

It must not directly decide the final result without deterministic validation.

45. LLM Matching Rule

Never send the entire candidate profile and ask:

"Is this candidate a good fit?"

That produces an opaque answer.

Instead provide:

specific requirement
+
specific candidate evidence

and ask:

Does this evidence satisfy this requirement?

This produces much more reliable results.

46. Example Semantic Check

Input:

Job requirement:
"Experience building REST APIs with Python."

Candidate evidence:
"Built FastAPI backend services for Teacher Progress Tracking."

Structured output:

{
  "relationship": "strongly_related",
  "status": "partial_match",
  "confidence": "high",
  "reason": "FastAPI is a Python web framework and the candidate has backend API implementation evidence."
}

The system can then decide the final status using deterministic rules.

47. No Hallucinated Candidate Evidence

The LLM must never produce:

Candidate has Kubernetes experience.

unless the candidate data actually contains evidence supporting it.

The prompt must explicitly state:

Candidate evidence supplied to the model is the complete evidence available for this comparison. Do not invent experience, skills, projects, certifications, employers, or achievements.

48. Candidate Data Isolation

Matching must always use:

authenticated candidate

and never:

candidate_id supplied by browser

without ownership validation.

Continue the Firebase Auth architecture from Phase 10.4.

49. Match Versioning

Use:

match_version

Example:

1.0

If matching rules change later:

1.1

Old results can remain for evaluation.

This is important because changing the algorithm can change results.

50. Input Versions

A match depends on:

job analysis version
candidate profile version
matching version

Store these references.

Example:

Job Analysis:
v1.2

Candidate Profile:
v3

Matching:
v1.0

This makes the result reproducible.

51. Stale Match Detection

Suppose:

Candidate adds:
Python

Existing match:

Candidate Profile version 2

is now stale.

The system should be able to determine:

current candidate version != match candidate version

and mark the result:

stale

or require recomputation.

Similarly:

JD changes
→ analysis changes
→ match becomes stale
52. Match Status

Suggested:

pending
computing
completed
failed
stale

Flow:

pending
 ↓
computing
 ↓
completed

If inputs change:

completed
 ↓
stale
53. API

Add:

POST /api/v1/jobs/{job_id}/match

This triggers matching for the authenticated candidate.

Do not accept arbitrary:

candidate_id

from the client.

54. Get Match
GET /api/v1/jobs/{job_id}/match

Return:

{
  "job_id": "...",
  "status": "completed",
  "overall_category": "strong_alignment",
  "summary": {
    "strong_matches": 7,
    "partial_matches": 2,
    "missing_required": 1,
    "preference_concerns": 1
  },
  "skill_matches": [],
  "experience": {},
  "education": {},
  "preferences": {}
}
55. Match Evidence Endpoint

Optional:

GET /api/v1/jobs/{job_id}/match/evidence

Useful for UI explanation.

Example:

React
Strong match

Why?
Candidate lists React and has project evidence.
56. Frontend Match UI

On the job detail page:

Your Fit
──────────────

Strong alignment

✓ React
✓ TypeScript
✓ Docker

△ Python
Partial match

✗ Kubernetes
Missing

Experience
✓ Meets requirement

Location
✓ Bengaluru

Work Mode
✓ Hybrid

Then:

Why this result?

The candidate should be able to inspect the evidence.

57. Important UX Rule

Never present:

You are rejected.

Instead:

Potential concern:
The job asks for 5+ years of experience.
Your profile currently shows 2.5 years.

The candidate still controls the application decision.

58. Required vs Preferred Display

Separate clearly:

Required
────────
✓ React
✓ TypeScript
△ Python

Preferred
────────
✓ AWS
✗ Docker

A missing preferred skill should not visually look like a failed mandatory requirement.

59. Matching Tests

Create comprehensive tests.

Exact skill
Job: React
Candidate: React

→ strong_match
Alias
Job: ReactJS
Candidate: React

→ strong_match
Related
Job: PostgreSQL
Candidate: MySQL

→ related/partial
Missing
Job: Kubernetes
Candidate: no Kubernetes evidence

→ missing
60. Experience Tests
Job:
2+ years

Candidate:
3 years

→ meets
Job:
5+ years

Candidate:
2 years

→ concern
Job:
2+ years

Candidate:
unknown

→ unknown
61. Education Tests

Test:

BCA
vs
Bachelor's degree in Computer Science or related field

The system should produce a qualified result rather than an absolute claim.

62. Preference Tests

Test:

Candidate:
Bengaluru
hybrid

Job:
Bengaluru
hybrid

→ aligned

Test:

Candidate:
Bengaluru only
remote/onsite preference rules
Job:
Mumbai onsite

→ concern
63. Evidence Tests

For every:

strong_match
partial_match
missing

verify that the system can explain the result.

Example:

React
→ candidate_skill_id exists

and:

Python
→ candidate evidence missing
64. No-Evidence Test

Candidate has no skills entered.

Job has:

React
Python
AWS

Expected:

unknown / missing evidence

Do not confidently state:

Candidate does not know React.

The distinction is important.

65. Candidate Claim vs Verified Evidence

If the candidate simply enters:

Python

this is:

candidate_claim

If Python appears in:

experience
project
certification
resume

confidence can be higher.

Do not call candidate claims false.

Just distinguish evidence strength.

66. Resume Evidence

A parsed resume may contain:

Python
FastAPI
AWS

Use that as supporting evidence if it is connected to the candidate.

However:

Parsed resume content is evidence, not automatically verified truth.

Do not silently upgrade every resume statement to verified experience.

67. Project Evidence

Example:

Project:
Teacher Progress Tracking

Technologies:
Angular
FastAPI
MySQL
Docker
AWS

Job:

FastAPI required

This is useful evidence.

The match explanation can say:

FastAPI appears in the candidate's project evidence.

68. Role Profile Matching

If the candidate has:

Frontend Engineer
Full Stack Engineer
FDE

the matching engine can compare the job to the candidate's active role profiles.

Example:

Job:
Forward Deployed Engineer

Candidate:
FDE role profile

→ strong role alignment.

This is one reason role profiles were created separately from the master profile.

69. Multiple Role Profiles

Do not force one global candidate role.

A candidate can have:

Role Profile A:
Frontend Engineer

Role Profile B:
Full Stack Engineer

Role Profile C:
Forward Deployed Engineer

A job can align differently with each.

Store:

best_matching_role_profile_id

or equivalent evidence if appropriate.

70. Important: Match Is Job-Specific

Do not create:

candidate_match_score

as a global candidate attribute.

Matching must be:

Candidate + Job

because the candidate can be:

excellent fit for Job A
average fit for Job B
poor fit for Job C
71. Match Result Example

For:

Frontend Engineer

result:

Overall:
Strong alignment

Required skills:
React       ✓
TypeScript  ✓
Angular     ✓
Python      △

Preferred:
AWS         ✓
Docker      ✓

Experience:
2+ years required
Candidate: 2.4 years
✓ Meets

Role:
Frontend Engineer
✓ Strong alignment

Location:
Bengaluru
✓ Preferred

Work mode:
Hybrid
✓ Aligned
72. Example With Gaps
Overall:
Good alignment with gaps

Required:
React       ✓
TypeScript  ✓
Python      ✗
PostgreSQL  △

Experience:
3+ years required
Candidate: 1.8 years
△ Concern

Preferred:
AWS         ✓
Docker      ✗

Recommendation:
Consider applying if the experience requirement is flexible.

The recommendation must remain informational.

73. No Automatic Rejection

The matching engine must never automatically prevent:

Apply
Save
Resume tailoring

because of a low match.

The candidate controls the decision.

74. Security

Protect:

candidate data
candidate resumes
candidate skills
candidate projects
match evidence

Only the authenticated candidate should access their private match details.

Shared job information can remain shared according to the existing authorization model.

75. Logging

Log:

candidate_id
job_id
match_version
analysis_version
status
duration

Do not log:

entire resumes
sensitive personal data unnecessarily
authentication tokens
LLM API keys
full private candidate profiles
76. Cost Control

Matching should avoid unnecessary LLM calls.

Use deterministic matching first.

Only invoke semantic AI when:

canonical IDs are insufficient

Example:

React ↔ React

requires no LLM.

But:

"RESTful API development"
↔
"FastAPI backend development"

may benefit from semantic evaluation.

77. Matching Pipeline

Final service flow:

Authenticated Candidate
        ↓
Load Candidate Profile
        ↓
Load Candidate Skills
        ↓
Load Experiences / Projects / Education
        ↓
Load Job
        ↓
Load JD Analysis
        ↓
Load Job Skills / Requirements
        ↓
Deterministic Matching
        ↓
Semantic Matching where necessary
        ↓
Evidence Generation
        ↓
Overall Categorization
        ↓
Persist JobMatch
        ↓
Persist MatchEvidence
78. No RAG Yet

Do not use:

Qdrant
embeddings
semantic vector retrieval

for the main matching engine in this phase.

The initial system should prove that structured matching works.

RAG/vector retrieval can later improve semantic retrieval and scale.

79. Acceptance Criteria

Phase 10.17 is complete only when:

 Candidate-job matching exists.
 Matching is candidate-specific.
 Matching is job-specific.
 Candidate ownership is enforced.
 Job analysis from 10.16 is consumed.
 Candidate skills are consumed.
 Skill aliases are reused.
 Exact skill matching works.
 Related skill relationships are distinguishable.
 Required vs preferred is preserved.
 Experience matching works.
 Education matching works.
 Certification matching works.
 Role profile alignment works.
 Location preference alignment works.
 Work-mode preference alignment works.
 Employment-type preference alignment works.
 Salary is treated as preference, not capability.
 Missing evidence is distinguished from confirmed absence where possible.
 Evidence is stored.
 Match versions are stored.
 Job-analysis version is stored.
 Candidate-profile version is stored.
 Stale matches can be identified.
 Matching is explainable.
 No fabricated candidate evidence is created.
 LLM is not the sole decision maker.
 No ATS score is falsely claimed.
 No resume generation occurs.
 No application submission occurs.
 No RAG/Qdrant implementation is introduced.
 Tests pass.
 Existing 10.1–10.16 functionality remains intact.