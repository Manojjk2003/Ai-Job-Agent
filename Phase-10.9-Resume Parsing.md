Phase 10.9 — Resume Parsing
# Phase 10.9 — Resume Parsing

## 1. Purpose

Phase 10.9 adds the ability to parse an uploaded resume and convert the document into structured, machine-readable information.

The previous phase, **10.8 Resume Upload**, only handled:

- Uploading the resume
- Validating the file
- Storing the file privately
- Saving resume metadata
- Listing resumes
- Downloading resumes
- Deleting resumes

This phase adds the next layer:

```text
Uploaded Resume
      ↓
File Validation
      ↓
Resume Parser
      ↓
Text Extraction
      ↓
Section Detection
      ↓
Structured Parsed Resume
      ↓
Candidate Review Later

The parsed resume becomes an input for later features such as:

Role Profiles
Resume Selection
Candidate Matching
Resume Tailoring
RAG
Career Assistant

However, this phase must NOT automatically modify the candidate's confirmed profile or skills.

2. Important Principle

The resume is a source of information, not automatically the source of truth.

For example, suppose a resume contains:

Skills:
Angular, TypeScript, Python, FastAPI, AWS

The parser can extract:

{
  "skills": [
    "Angular",
    "TypeScript",
    "Python",
    "FastAPI",
    "AWS"
  ]
}

But the system must NOT automatically assume that every extracted item is a confirmed candidate skill.

The correct future flow is:

Resume
   ↓
Parse
   ↓
Extracted Information
   ↓
Candidate Review
   ↓
Candidate Confirms / Edits
   ↓
Candidate Profile

This prevents the system from inventing or incorrectly adding experience.

3. Scope
Included

This phase includes:

PDF text extraction
DOCX text extraction
Resume section detection
Structured parsed representation
Parsing status
Parser metadata/version
Parse error handling
Persistence of parsed output
Re-parsing support
API endpoints
Candidate ownership/security
Frontend parsed-resume preview
Automated tests
4. Explicitly NOT Included

Do NOT implement the following in Phase 10.9:

AI resume rewriting
Resume tailoring
Job matching
ATS scoring
Skill-gap analysis
Job description analysis
RAG
Vector embeddings
Qdrant indexing
Career Assistant
Automatic profile updates
Automatic skill confirmation
Resume generation
Resume optimization
Automatic claims that a candidate possesses a skill
OCR implementation unless separately approved
External resume parsing APIs

These belong to later phases.

5. Why Resume Parsing Is Needed

The uploaded file itself is difficult for the application to reason over.

For example:

Manoj Kandagallmath
Junior Software Engineer

Experience
Software Engineer
Company A
2025 - Present

Skills
Angular
TypeScript
Python
FastAPI
MySQL
AWS

The application needs to transform this into something like:

{
  "name": "Manoj Kandagallmath",
  "headline": "Junior Software Engineer",
  "sections": {
    "experience": "...",
    "skills": "...",
    "education": "..."
  }
}

Later systems can then use these structured sections.

6. Architecture

The architecture is:

Angular Frontend
       |
       v
FastAPI Resume API
       |
       v
Resume Service
       |
       v
Resume Parser
   /          \
PDF Parser   DOCX Parser
   |             |
PyMuPDF      python-docx
   \             /
    \           /
     Parsed Resume
          |
          v
PostgreSQL

The original uploaded file remains in private storage.

The parsed representation is stored separately.

7. Technology

Use the already approved stack.

PDF

Use:

PyMuPDF

Python import:

import fitz

PyMuPDF should be used for deterministic PDF text extraction.

DOCX

Use:

python-docx

Example:

from docx import Document

Do not introduce another document parsing framework without approval.

8. Parsing Philosophy

The parser should be deterministic first.

Do not use Gemini simply to extract basic document text.

The initial pipeline should be:

File
 ↓
Read document
 ↓
Extract text
 ↓
Normalize text
 ↓
Detect sections
 ↓
Create structured representation
 ↓
Persist

AI can be introduced later for higher-level reasoning.

9. Supported File Types

Phase 10.8 supports:

PDF
DOCX

Therefore Phase 10.9 must support:

application/pdf
application/vnd.openxmlformats-officedocument.wordprocessingml.document

Do not add:

.doc
.txt
.rtf
images

unless separately approved.

10. Resume Parsing States

Introduce controlled parsing states.

Recommended values:

NOT_PARSED
PARSING
PARSED
FAILED

Meaning:

NOT_PARSED

The resume exists but has never been parsed.

PARSING

A parsing operation is currently running.

PARSED

Parsing successfully completed.

FAILED

The parser could not successfully extract usable content.

11. Database Design

The original resumes table from Phase 10.8 remains the source record for the uploaded file.

Do NOT recreate the resumes table.

Add a parsed representation linked to the resume.

Recommended table:

resume_versions

Relationship:

Candidate
   |
   +---- Resume
            |
            +---- ResumeVersion

One resume may have multiple parsing versions.

This allows future parser improvements without destroying previous results.

12. resume_versions Table

Recommended fields:

resume_versions
-------------------------------
id
resume_id
version_number
parse_status
parser_name
parser_version
extracted_text
structured_sections
text_hash
error_message
created_at
updated_at
parsed_at
id

UUID primary key.

resume_id

Foreign key to:

resumes.id

Use cascade behavior consistent with the existing resume ownership design.

version_number

Integer.

Example:

1
2
3

The first successful parsing attempt can create version 1.

A future re-parse can create version 2.

parse_status

Controlled enum/string:

NOT_PARSED
PARSING
PARSED
FAILED
parser_name

Example:

pymupdf
python-docx
parser_version

Store the parser/application parser version.

Example:

resume-parser-v1

This helps later when parsing logic changes.

extracted_text

The normalized text extracted from the resume.

structured_sections

JSON/JSONB representation of detected sections.

Example:

{
  "summary": "...",
  "skills": "...",
  "experience": "...",
  "education": "...",
  "projects": "...",
  "certifications": "...",
  "achievements": "..."
}
text_hash

SHA-256 hash of normalized extracted text.

Useful for detecting whether parsing results actually changed.

error_message

Stores a safe parsing error message.

Do not store secrets or credentials.

created_at

Creation timestamp.

updated_at

Last update timestamp.

parsed_at

Time when parsing completed successfully.

13. Why Use resume_versions?

Do not overwrite the previous parsed result every time.

For example:

Resume file
     |
     +-- Version 1
     |
     +-- Version 2
     |
     +-- Version 3

Suppose the parser is improved later.

The same uploaded resume could be parsed again using:

resume-parser-v2

The system can compare:

Version 1
vs
Version 2

This is useful for debugging and future evaluation.

14. Structured Sections

The parser should recognize common resume sections.

Recommended canonical section names:

contact
summary
objective
experience
education
skills
projects
certifications
achievements
awards
publications
languages
volunteering
other

Not every resume will contain every section.

Example:

{
  "summary": "...",
  "experience": "...",
  "skills": "...",
  "education": "...",
  "projects": "..."
}

Missing sections should simply be absent or represented as null/empty according to the schema.

15. Section Detection

Section detection should be heuristic and deterministic.

Common headings include:

Experience
Work Experience
Professional Experience
Employment
Education
Academic Background
Skills
Technical Skills
Projects
Personal Projects
Certifications
Certificates
Achievements
Awards
Summary
Professional Summary
Objective

The parser should normalize heading variations to canonical names.

Example:

WORK EXPERIENCE
Professional Experience
Employment History

can all map to:

experience

Similarly:

TECHNICAL SKILLS
Skills
Core Competencies

can map to:

skills
16. Important Parsing Rule

Do not attempt to understand the semantic truth of the content.

For example:

Resume text:

Worked with AWS for 2 years.

The parser should preserve this text.

It should NOT decide:

candidate_skill = AWS
years_experience = 2
proficiency = advanced

That is a later extraction/confirmation process.

17. Text Extraction
PDF

Use PyMuPDF.

Conceptually:

document = fitz.open(file_path)

pages = []

for page in document:
    pages.append(page.get_text())

text = "\n".join(pages)

The actual implementation must handle:

Empty pages
Page ordering
Encoding
File closing
Exceptions
Corrupt PDFs

Do not expose internal file paths to API users.

18. DOCX Extraction

Use python-docx.

Extract:

Paragraph text
Table text where practical

Resume documents frequently use tables for layout.

The parser should therefore inspect tables rather than only paragraphs.

Example conceptual output:

Paragraph 1
Paragraph 2
Table cell 1
Table cell 2

Preserve sensible reading order.

Do not attempt to reproduce the visual layout exactly.

The goal is machine-readable text.

19. Text Normalization

After extraction, normalize the text.

Possible operations:

Normalize line endings
Remove excessive blank lines
Normalize whitespace
Preserve meaningful bullets
Preserve section boundaries
Remove obviously empty lines

Do NOT aggressively modify the original wording.

For example:

Angular   TypeScript

should not become a completely different sentence.

The parser is extracting, not rewriting.

20. Structured Parsed Output

Example:

{
  "document": {
    "format": "pdf",
    "page_count": 2
  },
  "sections": {
    "contact": "...",
    "summary": "...",
    "experience": "...",
    "skills": "...",
    "projects": "...",
    "education": "..."
  }
}

The exact schema should remain extensible.

Do not create rigid fields for every possible resume detail at this stage.

21. Parsing Service

Create:

backend/app/services/resume_parser_service.py

Responsibilities:

load resume
validate supported format
select parser
extract text
normalize text
detect sections
calculate hash
return parsed representation

It should not:

modify candidate profile
create candidate skills
call Gemini
perform job matching
access Qdrant
22. Parser Abstraction

Use an abstraction so the application does not become tightly coupled to one parser.

Recommended structure:

backend/app/parsers/
    __init__.py
    base.py
    pdf_parser.py
    docx_parser.py

Example conceptual interface:

class ResumeParser:
    def parse(self, file_path: str) -> ParsedResume:
        ...

Then:

PDFResumeParser
DOCXResumeParser

implement the interface.

23. Parser Selection

The service should select the parser based on validated file type.

Conceptually:

PDF
 ↓
PDFResumeParser

DOCX
 ↓
DOCXResumeParser

Do not trust only the filename extension.

Phase 10.8 already performs file validation.

Phase 10.9 should still defensively verify the actual file type where practical.

24. API Endpoints

Add:

POST /api/v1/resumes/{resume_id}/parse

Starts parsing for the candidate's resume.

Response example:

{
  "id": "resume-version-uuid",
  "resume_id": "resume-uuid",
  "version_number": 1,
  "parse_status": "PARSED",
  "parser_name": "pymupdf",
  "parser_version": "resume-parser-v1",
  "parsed_at": "..."
}
25. Get Latest Parsed Resume

Add:

GET /api/v1/resumes/{resume_id}/parsed

Returns the latest parsed representation.

Example:

{
  "resume_id": "...",
  "version_number": 1,
  "parse_status": "PARSED",
  "structured_sections": {
    "summary": "...",
    "experience": "...",
    "skills": "...",
    "education": "..."
  }
}
26. List Parse Versions

Add:

GET /api/v1/resumes/{resume_id}/versions

Example:

[
  {
    "id": "...",
    "version_number": 1,
    "parse_status": "PARSED",
    "parser_version": "resume-parser-v1",
    "created_at": "..."
  }
]
27. Get Specific Parse Version

Add:

GET /api/v1/resumes/{resume_id}/versions/{version_id}

This allows the user/system to inspect a specific parsed result.

28. Re-parsing

The same endpoint:

POST /api/v1/resumes/{resume_id}/parse

may be used to re-parse.

For example:

First parse
    ↓
Version 1

Parser improved
    ↓
Second parse
    ↓
Version 2

Do not overwrite Version 1.

29. Candidate Ownership

Every endpoint must enforce ownership.

The candidate is identified from:

Firebase Auth token
        ↓
verified Firebase UID
        ↓
candidate record

Never accept:

candidate_id

from the browser as the authority for ownership.

For example, this is NOT sufficient:

POST /api/v1/resumes/{resume_id}/parse?candidate_id=abc

The backend must determine the authenticated candidate itself.

30. Authorization Flow
Request
   ↓
Firebase Bearer Token
   ↓
Verify Firebase token
   ↓
Resolve Firebase UID
   ↓
Resolve candidate
   ↓
Load resume
   ↓
Check resume.candidate_id
   ↓
Allow / Reject

If the resume belongs to another candidate:

403 Forbidden

Do not leak whether another user's resume exists if the API design uses a not-found response for ownership isolation.

Follow the existing security conventions from previous phases.

31. Parsing Errors

Examples:

Corrupt PDF
Unsupported DOCX structure
Empty document
No extractable text
Unexpected parser exception

The API should return a safe error.

Example:

{
  "parse_status": "FAILED",
  "error": "Resume text could not be extracted."
}

Do not expose Python stack traces.

Detailed errors should remain in server logs.

32. Empty Resume Handling

If the document contains no meaningful text:

PARSED

should NOT be returned.

Use:

FAILED

or an explicitly designed empty-content state if the implementation requires it.

For MVP, FAILED with a clear error is sufficient.

33. Security

Resume files may contain:

Name
Email
Phone
Address
Employment information
Education
Links
Other personal information

Therefore:

Keep original files private.
Keep parsed text private.
Enforce candidate ownership.
Do not expose storage paths.
Do not log entire resume contents.
Do not log extracted personal information unnecessarily.
Do not put parsed resume text into frontend logs.
Do not expose internal exceptions.
Do not make parsed files publicly accessible.
34. Prompt Injection Consideration

Although Phase 10.9 does not use an LLM, resume text should still be treated as untrusted external content.

For example, a resume could contain:

IGNORE ALL SYSTEM INSTRUCTIONS

The parser should simply treat this as text.

It must not execute instructions found inside the resume.

Later, when resume text is sent to an LLM, the system must explicitly treat it as untrusted document content.

35. Storage Considerations

The original resume remains in:

private object/local storage

The parser reads the file from that storage.

Do not create a public URL merely to parse the document.

Flow:

Private Resume
      ↓
Backend
      ↓
Parser
      ↓
Parsed Text

not:

Private Resume
      ↓
Public URL
      ↓
Parser
36. Frontend

Add a resume parsing experience to the existing resume UI.

Example:

My Resumes

resume.pdf
PDF
Uploaded: 04 Oct 2026

Status: Uploaded

[Parse Resume]

After parsing:

resume.pdf

Parsing Status: Parsed

[View Parsed Resume]
[Re-parse]
37. Parsed Resume View

Display sections such as:

Parsed Resume

Summary
----------------
...

Experience
----------------
...

Skills
----------------
...

Projects
----------------
...

Education
----------------
...

This is a preview.

Do not present extracted information as confirmed candidate profile data.

Use wording such as:

Extracted from resume

rather than:

Your verified skills
38. UX Principle

The user should understand the distinction between:

Resume content

and:

Confirmed profile

For example:

Extracted from your resume

Angular
Python
FastAPI
AWS

Later, the system can ask:

Confirm these skills?

That confirmation belongs to a later phase.

39. Backend Structure

Expected additions:

backend/app/
├── parsers/
│   ├── __init__.py
│   ├── base.py
│   ├── pdf_parser.py
│   └── docx_parser.py
│
├── services/
│   ├── resume_service.py
│   └── resume_parser_service.py
│
├── repositories/
│   └── resume_version_repository.py
│
├── schemas/
│   └── resume_version.py
│
└── api/
    └── v1/
        └── resumes.py

Use the existing architecture and naming conventions.

Do not restructure unrelated modules.

40. Repository Responsibilities

The repository should handle database operations such as:

create version
get latest version
get version
list versions
update parse status

The repository should not contain:

PDF parsing logic
DOCX parsing logic
authentication logic
LLM logic
41. Service Responsibilities

The service coordinates:

ownership
 ↓
resume lookup
 ↓
storage retrieval
 ↓
parser selection
 ↓
parsing
 ↓
normalization
 ↓
persistence

This keeps business logic outside the API route.

42. Schema Responsibilities

Pydantic schemas should define API contracts.

Example response:

ResumeVersionResponse

Possible fields:

id
resume_id
version_number
parse_status
parser_name
parser_version
structured_sections
parsed_at
created_at

Do not expose internal storage implementation details.

43. Database Migration

Create an Alembic migration for:

resume_versions

The migration must:

Create table
Add primary key
Add foreign key
Add indexes where appropriate
Add timestamps
Add parse status
Add version number
Add unique constraint for (resume_id, version_number)

Do not manually edit the existing migration history.

44. Indexes

At minimum consider:

resume_id
parse_status

The most important lookup is:

resume_id → latest version

An index should support this efficiently.

45. Version Number

Version numbering should be generated by the backend.

Do not trust a frontend-supplied:

version_number

The backend should determine:

latest version + 1

with appropriate handling for concurrent parsing requests.

46. Duplicate Parsing Requests

The system should avoid creating multiple versions accidentally when the same request is submitted repeatedly.

For MVP, the backend should prevent an uncontrolled number of simultaneous parse operations.

At minimum:

If status = PARSING
    reject or return current parsing state

Do not start unlimited duplicate parsing jobs.

47. Synchronous vs Background Parsing

For MVP, parsing may be synchronous if the files are small and processing is fast.

Flow:

POST /parse
    ↓
parse file
    ↓
save result
    ↓
return response

However, the service should be designed so it can later move to:

FastAPI
   ↓
Background Job
   ↓
Resume Parser

Do not introduce Celery/Redis merely for this phase.

Use the existing MVP architecture.

48. File Size

Respect the upload limits established in Phase 10.8.

Do not introduce a second conflicting file-size configuration.

The parser should defensively reject files that exceed the configured safety limit if necessary.

49. Parser Tests

Create unit tests for PDF parsing.

Test:

valid PDF
multiple pages
empty PDF
PDF with section headings
PDF with bullet points
corrupt PDF
50. DOCX Tests

Test:

valid DOCX
multiple paragraphs
tables
section headings
empty DOCX
corrupt DOCX
51. Section Detection Tests

Test:

Experience
WORK EXPERIENCE
Professional Experience
Employment History

all map to:

experience

Similarly test:

Technical Skills
Skills
Core Skills

mapping to:

skills
52. API Tests

Test:

Authentication

Unauthenticated request:

401
Ownership

Candidate A cannot parse Candidate B's resume.

Expected:

403

or the repository's existing ownership-isolation response convention.

Successful Parsing

Expected:

200/201

with:

PARSED
Invalid Resume

Expected:

FAILED

with a safe error response.

53. Integration Test

At least one integration flow should cover:

Create candidate
     ↓
Upload resume
     ↓
Parse resume
     ↓
Fetch parsed resume
     ↓
Verify structured sections

This validates that:

Storage
+
Database
+
Parser
+
API

work together.

54. Important Test

Verify that parsing does NOT modify candidate profile skills.

Before:

candidate_skills = []

After parsing:

candidate_skills = []

This is intentional.

Parsing creates extracted information only.

55. No AI Test

The resume parser should work even if:

Gemini credentials are unavailable

because Phase 10.9 is deterministic document parsing.

This makes the feature:

cheaper
testable
predictable
easier to debug
56. Logging

Log operational information such as:

resume_id
candidate_id
parser type
parse status
duration
error category

Do NOT log:

full resume text
full extracted resume
phone number
email
personal address

unless explicitly required for debugging and appropriately protected.

57. Observability

Measure:

parse duration
parse success rate
parse failure rate
document type
parser version

These metrics will become useful later when evaluating parser quality.

58. Parser Quality

A successful parser should not only mean:

No Python exception

It should also produce meaningful content.

At minimum:

extracted_text.strip() != ""

should be checked.

Later we can introduce more sophisticated parser-quality evaluation.

59. OCR

Scanned PDFs are a special case.

For example:

PDF
 └── image of resume

PyMuPDF may extract little or no text.

For Phase 10.9:

Detect
 ↓
No meaningful text
 ↓
Mark parsing failed / unsupported

Do not add OCR unless explicitly approved.

Future architecture may add:

OCR Provider

without changing the rest of the resume pipeline.

60. AI Boundary

The architecture should remain:

Document Parsing
       ↓
Structured Text
       ↓
Future AI Extraction
       ↓
Candidate Confirmation

Do not combine these layers.

This separation is important because:

Parser

Answers:

What text is physically present in the document?

AI extraction

Later answers:

What entities, skills, experiences, and claims appear to be represented by this text?

Candidate confirmation

Answers:

Which of those extracted facts are actually confirmed by the candidate?

These are three different responsibilities.

61. Data Flow

Complete Phase 10.9 flow:

Candidate
   |
   | Uploads Resume
   v
Resume Record
   |
   v
Private Storage
   |
   | POST /resumes/{id}/parse
   v
Resume Parser Service
   |
   +-------------------+
   |                   |
   v                   v
PDF Parser          DOCX Parser
   |                   |
   +---------+---------+
             |
             v
       Extracted Text
             |
             v
       Text Normalizer
             |
             v
       Section Detector
             |
             v
       Structured Resume
             |
             v
       Resume Version
             |
             v
        PostgreSQL
62. Example

Suppose the uploaded resume contains:

MANOJ K

Software Engineer

SUMMARY
Software engineer experienced in building web applications.

SKILLS
Angular, TypeScript, Python, FastAPI, MySQL, AWS

EXPERIENCE
Software Engineer
ABC Company
2025 - Present

PROJECTS
Teacher Progress Tracking
Built an application using Angular and FastAPI.

EDUCATION
BCA
Oxford College

The parser should produce something similar to:

{
  "sections": {
    "summary": "Software engineer experienced in building web applications.",
    "skills": "Angular, TypeScript, Python, FastAPI, MySQL, AWS",
    "experience": "Software Engineer\nABC Company\n2025 - Present",
    "projects": "Teacher Progress Tracking\nBuilt an application using Angular and FastAPI.",
    "education": "BCA\nOxford College"
  }
}

The parser should NOT automatically create:

Angular skill
Python skill
FastAPI skill

in the candidate profile.

64. RAG Boundary

Do NOT add Qdrant indexing in this phase.

The future flow will be:

Resume Parsing
      ↓
Structured Resume
      ↓
RAG Indexing
      ↓
Qdrant

Phase 10.9 stops at:

Structured Resume
      ↓
PostgreSQL
65. Gemini Boundary

Do NOT call Gemini for basic extraction.

Later Gemini-based processing may be used for:

skill extraction
experience extraction
achievement extraction
role classification
resume understanding

But those must operate on the parsed text.

Architecture:

PDF/DOCX
   ↓
Deterministic Parser
   ↓
Text
   ↓
AI Extraction

not:

PDF/DOCX
   ↓
Gemini directly
66. Acceptance Criteria

Phase 10.9 is complete only when:

 PDF resumes can be parsed.
 DOCX resumes can be parsed.
 Text extraction works.
 Section detection works for common headings.
 Parsed results are persisted.
 Resume versions are supported.
 Parser status is tracked.
 Parser version is stored.
 Parse failures are handled safely.
 Candidate ownership is enforced.
 No public resume URLs are introduced.
 Parsed text is not unnecessarily logged.
 Candidate profile is NOT automatically modified.
 Candidate skills are NOT automatically created.
 Gemini is NOT required.
 Qdrant is NOT required.
 API tests pass.
 Parser unit tests pass.
 Integration test passes.
 Angular build passes.
 Backend tests pass.
 Alembic migration passes.
 Existing functionality remains working.
67. Validation Checklist

Before declaring the phase complete:

Backend
[ ] Python compile
[ ] Unit tests
[ ] API tests
[ ] Integration tests
[ ] Alembic migration
[ ] Existing tests still pass

Frontend
[ ] Angular build
[ ] Resume parse UI works
[ ] Parsed result UI works

Security
[ ] Firebase authentication
[ ] Candidate ownership
[ ] Private storage
[ ] No path traversal
[ ] No sensitive logging

Parsing
[ ] PDF
[ ] DOCX
[ ] Multiple pages
[ ] Tables
[ ] Section detection
[ ] Empty documents
[ ] Corrupt documents
68. Implementation Rule for Codex

Implement this phase sequentially.

Before writing code:

Read the existing Phase 10.8 implementation.
Inspect the existing repository.
Inspect the existing resumes model/table.
Inspect the existing storage abstraction.
Inspect existing authentication and ownership logic.
Inspect existing API/router conventions.
Inspect existing tests.

Then implement Phase 10.9.

Do NOT recreate functionality already implemented in Phase 10.8.

Do NOT redesign the architecture.

Do NOT replace:

Angular
FastAPI
PostgreSQL
Firebase Authentication
existing storage abstraction

Do NOT introduce:

microservices
Redis
Celery
Kafka
Qdrant
Gemini
external resume parsing APIs

for this phase.

69. Implementation Order

Follow this order:

1. Inspect Phase 10.8
        ↓
2. Add resume_versions migration/model
        ↓
3. Add parser abstraction
        ↓
4. Add PDF parser
        ↓
5. Add DOCX parser
        ↓
6. Add text normalization
        ↓
7. Add section detection
        ↓
8. Add parser service
        ↓
9. Add repository
        ↓
10. Add schemas
        ↓
11. Add API endpoints
        ↓
12. Add frontend service
        ↓
13. Add frontend UI
        ↓
14. Add unit tests
        ↓
15. Add API/integration tests
        ↓
16. Run migrations
        ↓
17. Run backend tests
        ↓
18. Run frontend build
        ↓
19. Inspect implementation
        ↓
20. Fix issues
        ↓
21. Final verification
70. Final Implementation Report Required

After implementation, provide:

1. Implemented

List exactly what was implemented.

2. Files Added

List every new file.

3. Files Modified

List every modified file.

4. Database

Explain:

table
columns
constraints
indexes
migration
5. Parser

Explain:

PDF parser
DOCX parser
normalization
section detection
error handling
6. APIs

List every endpoint.

7. Frontend

Explain the resume parsing UI.

8. Security

Explain authentication and ownership enforcement.

9. Tests

Provide actual results:

Backend tests: X passed
Frontend build: PASS/FAIL
Migration: PASS/FAIL
Integration tests: X passed
10. Warnings

List warnings separately.

11. Errors

List unresolved errors separately.

12. Deviations

If anything differs from this document, explain:

Expected:
...

Implemented:
...

Reason:
...

Do not silently change architecture.

13. Remaining Work

Explicitly state that Phase 10.10 and later have NOT been implemented.

71. Phase Boundary

The final boundary is:

10.8 Resume Upload
        ↓
10.9 Resume Parsing
        ↓
10.10 Role Profiles
        ↓
10.11 Preferences
        ↓
...

Phase 10.9 ends after the application can reliably transform:

PDF/DOCX

into:

structured parsed resume data

while preserving the distinction between:

Extracted Resume Information

and:

Confirmed Candidate Profile Information

That distinction must remain intact for the rest of the system.


### What we are doing here

The important architectural decision in **10.9** is that we're separating three things:

**1. Parsing**
> “What text is actually inside this resume?”

**2. AI extraction later**
> “What skills, experiences, achievements, etc. does this text appear to describe?”

**3. Candidate confirmation**
> “Is this actually true and should it become part of my profile?”

That separation is important for your product because we **cannot allow the AI to invent skills just because something appears semantically similar**.

Next in the sequence is **Phase 10.10 — Role Profiles**.
