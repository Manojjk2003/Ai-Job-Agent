Phase 10.8 — Resume Upload
1. Purpose

Phase 10.8 introduces secure resume file upload and management for the Career Agent.

The candidate should be able to upload their existing resume and have the application securely store the original file.

The uploaded resume will later become the input for:

Resume parsing
Candidate profile extraction
Skill extraction
Resume analysis
Resume versioning
Resume tailoring
RAG indexing
Resume selection

However, those capabilities belong to later phases.

Phase 10.8 establishes only the secure resume file management foundation.

2. Scope

Phase 10.8 includes:

Resume upload
Resume metadata
Private file storage
Resume listing
Resume retrieval/download through controlled access
Resume deletion
File validation
Candidate ownership
Upload limits
Secure storage abstraction
Database persistence
API tests
Frontend upload UI

Phase 10.8 does not include:

Resume parsing
AI extraction
Skill extraction
Resume scoring
Resume tailoring
RAG indexing
Resume generation
Job matching

Those belong to later phases.

3. Architecture

The resume file itself must not be stored inside PostgreSQL.

Use:

Angular
   ↓
FastAPI
   ↓
Resume Service
   ↓
Private Object Storage
   ↓
Resume File

PostgreSQL stores metadata:

Resume
 ├── candidate_id
 ├── filename
 ├── storage_key
 ├── MIME type
 ├── size
 ├── status
 └── timestamps

The actual PDF/DOCX file remains in private object storage.

4. Storage Architecture

The approved architecture allows:

Firebase Storage
S3-compatible object storage

The implementation must use a storage abstraction rather than coupling the Resume Service directly to one provider.

Example:

StorageProvider
       │
       ├── FirebaseStorageProvider
       │
       └── S3StorageProvider

The application code should depend on:

StorageProvider

rather than directly depending on Firebase Storage or AWS S3 APIs.

This allows the storage implementation to change later without changing resume business logic.

5. Local Development

Because the MVP is intended to work locally/free initially, the implementation should support a local development storage strategy where appropriate.

For example:

LocalStorageProvider

may store files under a configured private application storage directory.

This must not expose files as a public static directory.

The production provider can later be:

S3StorageProvider

or:

FirebaseStorageProvider

depending on the deployment decision.

6. Important Security Principle

Resume files contain personal information.

Therefore:

Resume files must never be publicly accessible.

Do NOT create:

/public/resumes/...

Do NOT expose:

http://backend/resumes/file.pdf

as an unauthenticated URL.

The frontend should never receive a permanent public storage URL.

7. Resume Entity

Create a resumes table.

Suggested fields:

id
candidate_id
original_filename
storage_key
mime_type
file_size
file_hash
status
created_at
updated_at

Optional future fields may include:

parsed_at
is_primary
version

but do not add unnecessary fields unless required by the approved architecture.

8. Resume Status

The resume should have a controlled status.

Initial statuses:

UPLOADED
DELETED
FAILED

Later parsing can introduce:

PARSING
PARSED
PARSE_FAILED

However, those parsing states should primarily belong to Phase 10.9.

For 10.8, the important state is:

UPLOADED
9. Candidate Ownership

Every resume belongs to exactly one candidate.

Relationship:

Candidate
   │
   └── 1:N Resume

A candidate may have multiple resumes.

For example:

Candidate
 ├── Frontend Resume
 ├── Full Stack Resume
 └── FDE Resume

This is important because later resume selection will choose the appropriate resume for a job.

10. Resume Metadata

The database should store metadata such as:

original_filename
mime_type
file_size
storage_key
file_hash

The database must not store the complete resume binary.

11. Supported File Types

For the MVP, support:

PDF
DOCX

Do not support arbitrary file uploads.

Reject unsupported formats such as:

.exe
.zip
.js
.html
.svg

unless explicitly added later.

12. MIME Validation

Do not rely only on the browser-provided MIME type.

The backend must validate:

Filename extension
Declared MIME type
File signature/content where practical

For example:

PDF
→ %PDF

DOCX files should be validated as the expected Office Open XML format.

The backend must not trust:

Content-Type: application/pdf

alone.

13. File Size Limit

Introduce a configurable maximum file size.

Example:

MAX_RESUME_FILE_SIZE_MB=10

The exact value should come from configuration rather than being hardcoded throughout the application.

If the file exceeds the limit:

HTTP 413 Payload Too Large

should be returned.

14. Filename Security

Never use the user's original filename directly as the storage path.

For example, do NOT create:

resumes/manoj_resume.pdf

as the actual storage key.

Instead generate a safe internal key.

Example:

candidate/{candidate_id}/resumes/{resume_uuid}.pdf

The original filename remains metadata.

15. Storage Key

The storage key should contain no user-controlled path traversal.

Never allow:

../../something

or:

C:\Windows\...

to become a storage location.

The application generates the storage key.

Example:

candidates/
  <candidate_uuid>/
    resumes/
      <resume_uuid>.pdf
16. File Hash

Calculate a cryptographic hash such as SHA-256.

Example:

file
 ↓
SHA-256
 ↓
file_hash

The hash can later help detect duplicate uploads.

It should not be treated as a security authorization mechanism.

17. Duplicate Resume Upload

For the MVP, the system should detect identical files using:

candidate_id
+
file_hash

If the candidate uploads exactly the same file again, the system should provide a clear response.

The implementation should avoid silently creating unnecessary duplicate records.

18. Upload Flow

The expected flow:

Candidate
   ↓
Select Resume
   ↓
Angular validates basic file information
   ↓
POST /api/v1/resumes
   ↓
Firebase authentication
   ↓
FastAPI verifies token
   ↓
Resolve Candidate
   ↓
Validate file
   ↓
Generate Resume UUID
   ↓
Generate storage key
   ↓
Calculate hash
   ↓
Store file
   ↓
Create Resume metadata
   ↓
PostgreSQL
   ↓
Return Resume metadata
19. Transaction Safety

File storage and database operations are two separate systems.

The implementation must account for failure between them.

Example:

Store file
   ↓
Database insert fails

The uploaded object must not become an orphaned file.

Likewise:

Database insert succeeds
   ↓
File storage fails

must not create a database record pointing to a missing file.

Use a controlled service flow with cleanup/rollback behavior.

20. Resume Service

Create:

resume_service.py

Responsibilities:

Validate resume
Generate storage key
Calculate hash
Store file
Create metadata
Handle duplicate detection
Delete file
Delete metadata
Retrieve metadata
Coordinate storage and database operations

Do not place this logic directly inside API routes.

21. Storage Service

Create a storage abstraction.

Example:

class StorageProvider:
    async def upload(...):
        ...

    async def download(...):
        ...

    async def delete(...):
        ...

    async def exists(...):
        ...

The exact interface should follow the project's existing async/sync conventions.

22. Local Storage Provider

For development, implement:

LocalStorageProvider

It should:

Store files in a configured private directory
Generate no public URLs
Prevent path traversal
Support upload
Support download
Support delete
Support existence checks

Example configuration:

STORAGE_PROVIDER=local
LOCAL_STORAGE_PATH=./storage

The storage directory should be included in .gitignore.

23. Future Production Provider

The architecture should allow:

STORAGE_PROVIDER=s3

or:

STORAGE_PROVIDER=firebase

later.

Do not implement both production providers unnecessarily in Phase 10.8 if the approved MVP only requires local storage.

The important requirement is the abstraction.

24. API Endpoints

Base:

/api/v1/resumes
Upload
POST /api/v1/resumes

Multipart form upload.

Authentication required.

List
GET /api/v1/resumes

Returns only the authenticated candidate's resumes.

Get metadata
GET /api/v1/resumes/{resume_id}

Returns metadata only.

Download
GET /api/v1/resumes/{resume_id}/download

Authentication required.

The backend verifies ownership before returning the file.

Do not expose the storage path.

Delete
DELETE /api/v1/resumes/{resume_id}

Authentication required.

The backend should:

Verify ownership
Delete storage object
Delete database metadata

If storage deletion fails, handle the failure safely rather than pretending deletion succeeded.

25. Download Security

A candidate must only be able to download their own resume.

Flow:

GET /resumes/{id}/download
        ↓
Firebase token
        ↓
Candidate
        ↓
Resume
        ↓
Verify resume.candidate_id
        ↓
StorageProvider.download()
        ↓
Stream file

Never do:

GET /download?storage_key=...

where the user can control the storage key.

26. Streaming

Large files should be streamed instead of loading the entire file unnecessarily into memory.

Use the framework's appropriate streaming/file response mechanism.

27. Response Headers

Downloads should use appropriate headers.

For example:

Content-Type
Content-Disposition

The original filename may be used in the download response after being safely encoded.

Do not trust it as a filesystem path.

28. Resume List Response

Example:

{
  "id": "...",
  "original_filename": "resume.pdf",
  "mime_type": "application/pdf",
  "file_size": 245678,
  "status": "UPLOADED",
  "created_at": "..."
}

Do not return:

storage_key

unless there is a specific internal need.

Do not return secrets or storage credentials.

29. Frontend

Create a resume management section in the Angular application.

Candidate should be able to:

Profile
   ↓
Resumes
   ↓
Upload Resume

Display:

Resume.pdf
PDF
245 KB
Uploaded: ...

with actions:

Download
Delete
30. Upload UI

The UI should:

Accept PDF/DOCX
Display selected filename
Display file size
Prevent obvious invalid files
Show upload progress where practical
Show success/failure state
Allow retry

Frontend validation is only a user-experience feature.

Backend validation remains authoritative.

31. Angular Service

Create a typed service such as:

resume.service.ts

Responsibilities:

upload
list
get metadata
download
delete

Do not put HTTP logic directly into the component.

32. No Public URLs

The Angular application must never assume:

resume.publicUrl

exists.

The frontend should request a controlled backend download.

This is important because resume files contain personal information.

33. Database Migration

Create an Alembic migration for:

resumes

Foreign key:

resumes.candidate_id
    →
candidates.id

Use appropriate indexing.

At minimum:

candidate_id

should be indexed.

34. Repository

Create:

resume_repository.py

Responsibilities:

Get resume
List candidate resumes
Create metadata
Delete metadata
Find duplicate hash

Repository must not perform file storage operations.

35. Schemas

Create appropriate response schemas.

For example:

ResumeResponse
ResumeListResponse

The upload itself is multipart rather than JSON.

36. Security Requirements

The implementation must enforce:

Firebase authentication
Candidate ownership
Private storage
File type validation
File size validation
Path traversal protection
Safe generated storage keys
No public resume URLs
No secrets in logs
No credentials in frontend
Safe download authorization
37. Logging

Logs should contain useful operational information without leaking sensitive resume content.

Safe:

Resume upload completed
candidate_id=<internal id>
resume_id=<internal id>
file_size=...

Avoid logging:

Resume contents
Firebase tokens
Storage credentials
Full sensitive paths
Personal data unnecessarily
38. Testing
Upload tests

Test:

Valid PDF upload
Valid DOCX upload
Invalid extension
Invalid MIME
Oversized file
Empty file
Duplicate file
Authorization tests

Test:

Candidate A cannot download Candidate B's resume.
Candidate A cannot delete Candidate B's resume.
Candidate A cannot retrieve Candidate B's resume metadata.
39. Storage Tests

Test:

Upload
Download
Delete
Exists
Invalid path
Path traversal attempt

Example malicious filename:

../../resume.pdf

must never escape the configured storage directory.

40. Database Tests

Verify:

Migration succeeds
Resume references Candidate
Candidate deletion handles resume metadata appropriately
Candidate ownership query works
Duplicate detection works
41. End-to-End Test

Verify:

Login
 ↓
Upload resume.pdf
 ↓
Database metadata created
 ↓
Private file exists
 ↓
List resumes
 ↓
Download resume
 ↓
File contents match uploaded file
 ↓
Delete resume
 ↓
Database record removed
 ↓
File removed
42. Failure Tests

Test:

Storage succeeds, DB fails

The uploaded file should be cleaned up.

Storage fails, DB should not claim success

No invalid resume record should remain.

Download storage object missing

Return an appropriate server error rather than returning a successful empty file.

43. No Resume Parsing

This is extremely important.

Do NOT implement:

PDF
 ↓
PyMuPDF
 ↓
Extract text

yet.

That is:

Phase 10.9 — Resume Parsing.

10.8 only stores the original file safely.

44. No AI

Do not use Gemini in Phase 10.8.

No:

Resume
 ↓
Gemini
 ↓
Extract profile

No AI is required for upload.

45. No RAG

Do not embed the resume into Qdrant yet.

The later flow will be:

Resume
 ↓
10.9 Parsing
 ↓
Structured content
 ↓
RAG indexing

The vector architecture is already defined in Phase 7.

46. No Resume Generation

Do not create a new resume in Phase 10.8.

This phase only manages uploaded source resumes.

Resume generation belongs to later phases.

47. Definition of Done

Phase 10.8 is complete when:

Backend
Resume model exists
Migration exists
Upload API works
List API works
Metadata API works
Download API works
Delete API works
Ownership is enforced
Validation works
Storage
Storage abstraction exists
Local storage works
Files remain private
Path traversal is prevented
Cleanup works
Frontend
Candidate can upload resume
Candidate can see uploaded resumes
Candidate can download
Candidate can delete
Errors are displayed correctly
Security
No public resume URLs
Candidate isolation works
File validation works
Storage keys are generated server-side
Testing
Backend tests pass
Storage tests pass
Authorization tests pass
API tests pass
Angular tests/build pass
48. Deliverables
Backend
├── Resume model
├── Resume repository
├── Resume service
├── StorageProvider
├── LocalStorageProvider
├── Resume schemas
├── Resume API routes
├── Alembic migration
└── Tests

Frontend
├── Resume management UI
├── Resume upload
├── Resume listing
├── Resume download
├── Resume deletion
├── Resume API service
└── Tests
49. Final Goal

At the end of Phase 10.8:

An authenticated candidate can securely upload, view, download, and delete their resumes while the application keeps the original files private and stores only resume metadata in PostgreSQL.

The next phase will then build on this:

10.8 Resume Upload
        ↓
10.9 Resume Parsing
        ↓
Extract resume content
        ↓
Candidate confirmation
        ↓
Profile / Skills evidence