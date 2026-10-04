import hashlib
from datetime import datetime,timezone
from fastapi import HTTPException
from app.db.models.resume_version import ResumeVersion
from app.repositories import resume_version_repository as repo
from app.services import resume_service
from app.parsers.resume import parse_pdf,parse_docx,sections
def parse(db,candidate_id,resume):
 last=repo.latest(db,resume.id)
 if last and last.parse_status=='PARSING':raise HTTPException(409,'Resume is already being parsed')
 version=ResumeVersion(resume_id=resume.id,version_number=(last.version_number if last else 0)+1,parse_status='PARSING');db.add(version);db.commit();db.refresh(version)
 try:
  path=resume_service.storage.read(resume.storage_key);text=parse_pdf(path) if resume.mime_type=='application/pdf' else parse_docx(path);text='\n'.join(x.rstrip() for x in text.splitlines()).strip()
  if not text:raise ValueError('Resume text could not be extracted.')
  version.parse_status='PARSED';version.parser_name='pymupdf' if resume.mime_type=='application/pdf' else 'python-docx';version.parser_version='resume-parser-v1';version.extracted_text=text;version.structured_sections=sections(text);version.text_hash=hashlib.sha256(text.encode()).hexdigest();version.parsed_at=datetime.now(timezone.utc)
 except Exception as e:version.parse_status='FAILED';version.error_message='Resume text could not be extracted.'
 db.commit();db.refresh(version);return version
