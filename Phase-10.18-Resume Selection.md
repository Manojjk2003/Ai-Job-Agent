1. Objective

Build a Resume Selection system that answers:

Given this job and this candidate, which existing resume/profile is the best truthful starting point?

A candidate may have multiple resumes:

Frontend Resume
Full Stack Resume
FDE Resume
General Software Engineer Resume

A single resume should not automatically be used for every job.

Example:

Job A:
Frontend Engineer
        ↓
Frontend Resume

Job B:
Forward Deployed Engineer
        ↓
FDE Resume

Job C:
Full Stack Engineer
        ↓
Full Stack Resume

The selection system must use the candidate's verified information and the job's requirements.

2. Phase Boundary

The pipeline is:

10.16 JD Analysis
        ↓
10.17 Candidate Matching
        ↓
10.18 Resume Selection
        ↓
10.19 Resume Tailoring
        ↓
10.20 Applications
10.17

Answers:

How well does the candidate fit the job?

10.18

Answers:

Which existing resume/profile is the best starting point?

10.19

Will later answer:

How should that selected resume be tailored for this specific JD?

3. Critical Product Principle

Resume selection must never create new candidate facts.

The source of truth remains:

Candidate Master Profile
        ↓
Role Profiles
        ↓
Existing Resume Versions

The selected resume is only a presentation strategy.

It must not change:

skills
experience
projects
education
certifications
achievements
4. Important Distinction

There are three different concepts:

Candidate Truth
       ↓
Role Profile
       ↓
Resume
Candidate Truth

Everything the candidate can legitimately claim.

Role Profile

A role-specific representation of that truth.

Examples:

Frontend Engineer
Full Stack Engineer
FDE
Resume

A document representing one particular positioning of the candidate.

5. Example

Candidate has:

Skills:
Angular
React
TypeScript
Python
FastAPI
MySQL
Docker
AWS

Projects:
TPT
SLH
KiddyPi

Role profiles:

Frontend Engineer
Full Stack Engineer
FDE

Job:

Forward Deployed Engineer

The system should prefer:

FDE Role Profile

and the corresponding resume.

It should not automatically select the generic resume simply because it contains more keywords.

6. Resume Selection Is Not Resume Generation

This phase must not:

rewrite resume
generate resume
add keywords
invent achievements
modify bullet points
reorder resume content for a JD
create a new PDF
generate DOCX
submit application

Those belong to later phases.

7. Existing Resume Domain

Reuse the resume entities created in:

10.8 Resume Upload
10.9 Resume Parsing

Do not recreate:

resumes
resume_versions

if they already exist.

Inspect the actual repository first.

8. Role Profile Domain

Reuse:

role_profiles
role_profile_skills
role_profile_experiences
role_profile_projects

from Phase 10.10.

Do not create duplicate role-profile data.

9. Selection Inputs

The selector should consider:

Job
Job Analysis
Candidate Profile
Role Profiles
Candidate Skills
Existing Resumes
Parsed Resume Versions
Candidate-Job Match

Primary inputs:

Job
+
JD Analysis
+
Candidate-Job Match
+
Role Profiles
+
Existing Resumes
10. Selection Output

The result should answer:

Selected resume:
FDE Resume

Selected role profile:
Forward Deployed Engineer

Why:
- Strong role alignment
- Highest coverage of required responsibilities
- Contains relevant implementation/project evidence
- Matches candidate's target role

Alternatives:
Full Stack Resume
Frontend Resume
11. Do Not Use Only Keyword Count

Bad implementation:

score = number_of_matching_keywords

This can produce incorrect results.

Example:

Resume A:
contains 15 occurrences of "Python"

Resume B:
contains Python + FastAPI + deployment + client implementation experience

For an FDE job, Resume B may be much better.

Selection should consider role positioning + evidence + job requirements.

12. Selection Dimensions

Evaluate candidate resume/profile candidates using:

Role alignment
Required skill coverage
Preferred skill coverage
Experience alignment
Project relevance
Responsibility alignment
Seniority alignment
Resume completeness
Resume parsing availability
Recency
Candidate preference alignment

Not all dimensions need equal weight.

13. Role Alignment

This should be one of the strongest signals.

Example:

Job:
Frontend Engineer

Role Profile:
Frontend Engineer

→ strong alignment

Example:

Job:
FDE

Role Profile:
Frontend Engineer

→ possible alignment

Example:

Job:
Backend Engineer

Role Profile:
Frontend Engineer

→ weak alignment
14. Job Title Normalization

Do not require exact title equality.

Examples:

Frontend Engineer
Frontend Developer
UI Engineer
Web Developer

may have meaningful overlap.

Use the job analysis and role profile rather than:

job.title == role_profile.target_designation
15. Required Skill Coverage

Suppose the job requires:

React
TypeScript
REST APIs
AWS
Docker

Resume/Profile A:

React
TypeScript
REST APIs

Resume/Profile B:

React
TypeScript
REST APIs
AWS
Docker

Prefer B.

But do not blindly choose the resume containing the most skills.

The skills must be relevant and supported by candidate truth.

16. Required vs Preferred

Separate:

Required skills

from:

Preferred skills

Required coverage should have higher importance.

Example:

Required:
React
TypeScript

Preferred:
GraphQL
Jest

A resume missing GraphQL should not automatically lose to one containing GraphQL if the second has poorer required-role alignment.

17. Experience Relevance

Consider which role profile/resume best represents the experience relevant to the job.

Example:

Job:
Forward Deployed Engineer

Relevant experience:
requirements gathering
HLD
LLD
data modeling
customer-facing implementation
deployment
debugging

A profile emphasizing these experiences is preferable to a purely frontend-focused profile.

18. Project Relevance

Projects should be considered as evidence.

Example:

Job:
Full Stack Engineer

Relevant:
Angular
FastAPI
MySQL
Docker
AWS
REST APIs

A resume/profile containing projects demonstrating these technologies is stronger.

Do not select based only on project title.

19. Resume Parsing Status

Only resumes with usable parsed content should be considered fully eligible for selection.

Possible states:

uploaded
parsed
failed
not_parsed

Preferred:

PARSED

If a resume has not been parsed:

selection_status:
incomplete

It may still be shown as an alternative, but should not silently receive full confidence.

20. Resume Version

A resume may have:

Resume
 ├── Version 1
 ├── Version 2
 └── Version 3

Select the appropriate current version.

Do not assume the newest upload is automatically the best.

21. Existing Resume vs Role Profile

These are different selection levels.

Example:

Job
 ↓
Role Profile:
FDE
 ↓
Resume:
FDE Resume v3

The system should ideally select both:

selected_role_profile
selected_resume
22. Why Store Both?

Suppose:

FDE Role Profile

exists but the candidate has:

FDE Resume v1
FDE Resume v2

The role profile explains:

Why this candidate positioning is appropriate.

The resume explains:

Which actual document should be used as the base.

23. Database Design

Create:

resume_selections

Suggested fields:

id
candidate_id
job_id
role_profile_id
resume_id
resume_version_id
status
selection_version
selection_method
confidence
reason_summary
created_at
updated_at

Possible status:

pending
completed
failed
stale
24. Selection Method

Support:

deterministic
semantic
hybrid
manual

MVP should primarily use:

hybrid

where:

structured rules
+
candidate/job evidence

are used.

25. Unique Selection

For a given:

candidate
+
job
+
selection_version

avoid duplicate active selection records.

Historical versions may remain.

26. Selection Evidence

Create:

resume_selection_evidence

Suggested fields:

id
resume_selection_id
evidence_type
source_entity_type
source_entity_id
dimension
result
reason
weight
created_at

Possible dimensions:

role_alignment
required_skill_coverage
preferred_skill_coverage
experience_alignment
project_relevance
responsibility_alignment
seniority_alignment
resume_completeness
27. Example Evidence
Dimension:
role_alignment

Selected:
FDE Role Profile

Reason:
Job title and responsibilities align with the candidate's FDE role profile.

Another:

Dimension:
required_skill_coverage

Resume:
FDE Resume v2

Reason:
Contains evidence for Python, FastAPI, REST APIs, Docker and AWS.
28. Selection Explanation

The user should see:

Why this resume?

✓ Best role alignment
✓ Covers most required skills
✓ Contains relevant project evidence
✓ Matches target seniority

Alternative:
Full Stack Resume
Good technical coverage, but weaker FDE positioning.

This is much more useful than:

Selected because score = 83.4
29. Numerical Score

A numerical internal score may be used.

If implemented, define it explicitly.

Example:

Role alignment             30%
Required skill coverage    30%
Experience relevance       20%
Project relevance          10%
Resume quality             10%

These values are only an example.

Do not blindly copy them.

The implementation must document the actual formula.

Never label it:

ATS score
30. Preferred MVP

For MVP, prefer:

Strong
Good
Possible
Weak
Insufficient data

instead of exposing an artificial percentage.

31. Candidate Match Reuse

Phase 10.17 already calculated:

candidate ↔ job

Do not recompute the entire match unnecessarily.

Resume selection should consume:

job_match
match_evidence

where applicable.

Example:

Job requires React
        ↓
10.17 determined candidate has strong React evidence
        ↓
10.18 evaluates which resume/profile presents that evidence appropriately
32. Important Difference

Matching asks:

Does the candidate have this capability?

Resume selection asks:

Which existing representation best communicates this capability for this job?

These are related but not identical.

33. Example

Candidate:

React
Python
FastAPI
AWS
Docker

Job:

FDE
Python
FastAPI
AWS
Docker
client implementation

Candidate matching:

Strong technical match

Resume selection:

FDE Resume

because it best communicates:

implementation
requirements
deployment
technical communication
34. Resume Selection Should Be Truth-Preserving

Suppose the job requires:

Kubernetes

and the candidate does not have Kubernetes.

Resume A:

does not mention Kubernetes

Resume B:

also does not mention Kubernetes

Do not prefer B merely because an unrelated keyword appears.

More importantly:

Never select a resume because it can be made to appear as though the candidate has Kubernetes.

35. Resume Claims

Use parsed resume information as evidence.

But remember:

Resume statement
≠
independently verified fact

The selection engine can use it as candidate-provided evidence.

Do not fabricate stronger evidence.

36. Multiple Candidate Resumes

Example:

Candidate
 ├── Frontend Resume v1
 ├── Frontend Resume v2
 ├── Full Stack Resume v1
 └── FDE Resume v3

The selector should evaluate all eligible resumes.

Return:

selected
alternatives
37. Archived Resume

If a resume is marked inactive/archived:

do not select it

unless explicitly requested by the candidate.

Historical application records may still reference it.

Do not delete historical resume records merely because they are no longer active.

38. Missing Resume

Suppose the candidate has:

FDE Role Profile

but no FDE resume.

The system should return:

No suitable existing resume found.
Recommended role profile:
FDE

Next action:
Create/tailor a resume from this role profile.

Do not generate the resume in this phase.

39. No Resume At All

If candidate has no usable resume:

status:
no_eligible_resume

The system should still identify:

best role profile

if one exists.

This prepares the system for 10.19.

40. No Role Profile

If no role profile exists:

status:
insufficient_positioning

Do not automatically invent one.

The system can say:

A role-specific profile is recommended before tailoring.
41. Fallback Strategy

Selection priority:

1. Eligible role-aligned resume
2. Strong job-match evidence
3. Required skill coverage
4. Relevant experience
5. Relevant projects
6. Resume completeness
7. Recency

Exact weighting must be documented.

42. Recency

Recency can matter.

Example:

Resume v1:
created 2025

Resume v2:
created 2026

If both are equally relevant:

v2

may be preferred.

But:

Newest does not automatically mean best.

43. Resume Completeness

Check whether the parsed resume contains usable sections:

summary
experience
skills
projects
education

A resume with only:

skills

should not necessarily beat a complete, relevant resume.

44. Manual Override

The candidate should eventually be able to override the recommendation.

Example UI:

Recommended:
FDE Resume v3

[Use recommended]

Other resumes:
Full Stack Resume v2
Frontend Resume v1

[Use this instead]

Manual selection should be recorded.

45. Manual Selection Is Not a System Failure

If candidate selects:

Frontend Resume

for an FDE job:

the system should not prevent it.

Instead record:

selection_method:
manual

and continue.

46. Selection API

Add:

POST /api/v1/jobs/{job_id}/resume-selection

This generates/recomputes the selection for the authenticated candidate.

No client-supplied candidate ID.

47. Get Selection
GET /api/v1/jobs/{job_id}/resume-selection

Response should include:

{
  "status": "completed",
  "selected_role_profile": {
    "id": "...",
    "name": "Forward Deployed Engineer"
  },
  "selected_resume": {
    "id": "...",
    "version_id": "..."
  },
  "confidence": "high",
  "reason_summary": "Best alignment with the job's role and requirements.",
  "alternatives": []
}
48. Manual Selection API

If supported:

POST /api/v1/jobs/{job_id}/resume-selection/manual

Request:

{
  "resume_id": "...",
  "resume_version_id": "...",
  "role_profile_id": "..."
}

Validate ownership.

The selected resume must belong to the authenticated candidate.

49. Frontend

On Job Detail:

Your Match
──────────────
Strong alignment

Selected Resume
──────────────
FDE Resume v3

Role Profile
──────────────
Forward Deployed Engineer

Why?
✓ Strong role alignment
✓ Relevant skills
✓ Relevant implementation experience

[Review Resume]
[Choose Another]

Do not show a "Tailor Resume" implementation yet.

The button can remain disabled or be prepared for Phase 10.19.

50. Resume Preview

If an existing preview system already exists, reuse it.

Do not build a full document editing system here.

The user only needs enough information to understand which resume was selected.

51. Stale Selection

Selection becomes stale if:

job changes
job analysis changes
candidate profile changes
role profile changes
resume version changes
matching version changes
selection algorithm changes

Store versions needed to detect this.

52. Example

Current:

Selected:
FDE Resume v3

Job Analysis:
v2

Candidate Profile:
v4

Selection:
v1

Candidate adds:

new FDE project

Candidate profile becomes:

v5

Existing selection should become:

stale

and can be recomputed.

53. AI Usage

AI should not simply receive:

candidate + job + resumes

and decide:

Use Resume B.

That is opaque.

Prefer:

Structured candidate/job facts
        ↓
Deterministic candidate set
        ↓
Compare role alignment
        ↓
Compare skill/evidence coverage
        ↓
Optional semantic evaluation
        ↓
Deterministic final selection
54. Optional Gemini Usage

Gemini may help with:

semantic role alignment
responsibility similarity
project relevance
ambiguous skill relationships

Example:

Job:
"Work directly with customers to implement technical solutions."

Candidate role profile:
FDE

Profile evidence:
requirements gathering
HLD
LLD
deployment
debugging

AI can assess semantic relevance.

But the model must only use supplied evidence.

55. Structured AI Output

If Gemini is used, require structured output similar to:

{
  "dimension": "role_alignment",
  "relationship": "strong",
  "confidence": "high",
  "reason": "..."
}

Do not accept free-form prose as the source of the final decision.

56. AI Guardrail

Prompt must explicitly say:

Do not invent skills.
Do not invent experience.
Do not invent projects.
Do not infer unprovided employment history.
Do not treat missing evidence as proof of absence.
Do not modify candidate facts.
57. No RAG

Do not introduce:

Qdrant
embeddings
vector search

for this phase.

The matching and selection system should initially operate on structured PostgreSQL data.

58. Testing

Create unit tests for:

role alignment
skill coverage
experience alignment
project relevance
resume completeness
recency
parsed/unparsed resume
archived resume
missing resume
missing role profile
manual selection
ownership
stale selection
59. Selection Test Example

Candidate:

Role Profiles:
Frontend
FDE

Job:

FDE

Resumes:

Frontend Resume
FDE Resume

Expected:

FDE Resume
60. Skill Coverage Test

Job:

Python
FastAPI
Docker
AWS

Resume A:

Python

Resume B:

Python
FastAPI
Docker
AWS

Expected:

Resume B

assuming role alignment is otherwise equivalent.

61. Role vs Keyword Test

Resume A:

contains many Python keywords

but role profile:

Frontend

Resume B:

contains fewer Python keywords

but role profile:

FDE

Job:

FDE

Expected:

Resume B

if its relevant evidence is stronger.

This prevents naive keyword-count selection.

62. Archived Resume Test

Resume:

status:
archived

Expected:

not eligible

unless manually selected through an explicitly supported historical workflow.

63. Ownership Test

Candidate A attempts:

POST /jobs/{job_id}/resume-selection

using Candidate B's resume ID.

Expected:

403 / 404

according to existing authorization conventions.

Never expose whether another candidate's resume exists if your API design treats that as sensitive.

64. Stale Test

Create selection:

candidate_profile_version = 3

Update candidate:

version = 4

Expected:

selection = stale

or equivalent recomputation behavior.

65. No Suitable Resume Test

Candidate:

has only archived resumes

Expected:

no_eligible_resume

and a useful explanation.

66. No Role Profile Test

Candidate:

no role profiles

Expected:

insufficient_positioning

rather than fabricated role selection.

67. Idempotency Test

Run:

POST /jobs/{job_id}/resume-selection

twice without changing inputs.

Expected:

same logical selection

and no uncontrolled duplicate active selections.

68. Security

Continue existing Firebase authentication.

Every private operation must derive:

candidate_id

from:

verified Firebase UID

Never trust:

candidate_id

from request body/query parameters.

69. Audit

Record important manual decisions.

Example:

candidate selected:
Frontend Resume v2

instead of recommended:

FDE Resume v3

This becomes useful later for understanding:

which resumes candidates actually prefer

and improving selection logic.

70. Future Learning Signal

Do not build machine-learning optimization yet.

But structure data so later the system can analyze:

recommended resume
chosen resume
application result
interview result
rejection

This can eventually help determine:

Which resume positioning performs better for which types of jobs?

That is a future learning system, not part of this phase.

71. Acceptance Criteria

Phase 10.18 is complete only when:

 Existing resume domain is reused.
 Existing role-profile domain is reused.
 Candidate-job match is reused.
 Resume selection is job-specific.
 Candidate ownership is enforced.
 Role alignment is considered.
 Required skill coverage is considered.
 Preferred skill coverage is considered.
 Experience relevance is considered.
 Project relevance is considered.
 Seniority alignment is considered.
 Resume parsing status is considered.
 Resume version is considered.
 Archived resumes are excluded.
 Missing resumes are handled gracefully.
 Missing role profiles are handled gracefully.
 Selection explanation is stored.
 Selection evidence is stored.
 Selection version is stored.
 Stale selection can be detected.
 Manual selection is supported or explicitly deferred with architecture preserved.
 AI cannot invent candidate facts.
 No resume content is rewritten.
 No new resume is generated.
 No application is submitted.
 No RAG/vector implementation is introduced.
 Tests pass.
 Existing functionality remains intact.