from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.resume import Resume
from app.db.models.resume_version import ResumeVersion
from app.db.models.resume_selection import ResumeSelection
def select(db:Session,candidate_id,job_id,resume_id=None):
 resume=db.query(Resume).filter(Resume.id==resume_id,Resume.candidate_id==candidate_id,Resume.status=='UPLOADED').first() if resume_id else db.query(Resume).filter(Resume.candidate_id==candidate_id,Resume.status=='UPLOADED').order_by(Resume.created_at.desc()).first()
 if not resume:raise HTTPException(404,'No eligible candidate-owned resume found')
 version=db.query(ResumeVersion).filter(ResumeVersion.resume_id==resume.id,ResumeVersion.parse_status=='PARSED').order_by(ResumeVersion.version_number.desc()).first();value=db.query(ResumeSelection).filter(ResumeSelection.candidate_id==candidate_id,ResumeSelection.job_id==job_id).first()
 if not value:value=ResumeSelection(candidate_id=candidate_id,job_id=job_id,resume_id=resume.id,resume_version_id=version.id if version else None,selection_method='manual' if resume_id else 'latest_eligible',explanation='Selected an eligible candidate-owned resume; no resume content was changed.');db.add(value)
 else:value.resume_id=resume.id;value.resume_version_id=version.id if version else None
 db.commit();db.refresh(value);return value
