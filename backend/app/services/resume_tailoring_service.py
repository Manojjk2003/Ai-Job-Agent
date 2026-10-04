import hashlib
from datetime import datetime,timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.resume_selection import ResumeSelection
from app.db.models.resume_version import ResumeVersion
from app.db.models.tailored_resume import TailoredResume,TailoredResumeClaim
def generate(db:Session,candidate_id,job_id):
 selection=db.query(ResumeSelection).filter(ResumeSelection.candidate_id==candidate_id,ResumeSelection.job_id==job_id).first()
 if not selection:raise HTTPException(409,'Resume selection is required before tailoring')
 version=db.get(ResumeVersion,selection.resume_version_id) if selection.resume_version_id else None
 if not version or not version.extracted_text:raise HTTPException(409,'A parsed selected resume version is required')
 text=version.extracted_text;digest=hashlib.sha256(text.encode()).hexdigest();previous=db.query(TailoredResume).filter(TailoredResume.candidate_id==candidate_id,TailoredResume.job_id==job_id,TailoredResume.source_hash==digest,TailoredResume.status=='review_required').first()
 if previous:return previous
 next_version=(db.query(TailoredResume).filter(TailoredResume.candidate_id==candidate_id,TailoredResume.job_id==job_id).count()+1);value=TailoredResume(candidate_id=candidate_id,job_id=job_id,resume_selection_id=selection.id,generation_version=next_version,source_hash=digest,structured_content={'source_resume_version_id':str(version.id),'text':text},validation_summary={'status':'passed','claim_policy':'verbatim parsed resume content only','gemini_used':False});db.add(value);db.flush();db.add(TailoredResumeClaim(tailored_resume_id=value.id,claim_text=text,source_type='resume_version',source_id=version.id));db.commit();db.refresh(value);return value
def get(db,candidate_id,job_id):
 value=db.query(TailoredResume).filter(TailoredResume.candidate_id==candidate_id,TailoredResume.job_id==job_id).order_by(TailoredResume.created_at.desc()).first()
 if not value:raise HTTPException(404,'Tailored resume not found')
 return value
def approve(db,candidate_id,job_id):
 value=get(db,candidate_id,job_id);value.status='approved';value.approved_at=datetime.now(timezone.utc);db.commit();db.refresh(value);return value
def reject(db,candidate_id,job_id,reason=None):
 value=get(db,candidate_id,job_id);value.status='rejected';value.rejected_at=datetime.now(timezone.utc);value.rejection_reason=reason;db.commit();db.refresh(value);return value
