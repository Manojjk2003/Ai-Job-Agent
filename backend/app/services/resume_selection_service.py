from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.resume import Resume
from app.db.models.resume_version import ResumeVersion
from app.db.models.resume_selection import ResumeSelection
from app.db.models.job_analysis import JobAnalysis,JobSkill
from app.db.models.skill import Skill
def _score(version, skill_names):
 text=(version.extracted_text or '').lower();covered=[name for name in skill_names if name.lower() in text];return len(covered)*10+(5 if version.structured_sections else 0),covered
def select(db:Session,candidate_id,job_id,resume_id=None):
 candidates=db.query(Resume).filter(Resume.candidate_id==candidate_id,Resume.status=='UPLOADED').all()
 if resume_id:candidates=[r for r in candidates if r.id==resume_id]
 options=[]
 analysis=db.query(JobAnalysis).filter(JobAnalysis.job_id==job_id,JobAnalysis.status=='completed').order_by(JobAnalysis.created_at.desc()).first();skill_names=[]
 if analysis:skill_names=list(db.scalars(__import__('sqlalchemy').select(Skill.name).join(JobSkill,JobSkill.skill_id==Skill.id).where(JobSkill.analysis_id==analysis.id)))
 for item in candidates:
  version=db.query(ResumeVersion).filter(ResumeVersion.resume_id==item.id,ResumeVersion.parse_status=='PARSED').order_by(ResumeVersion.version_number.desc()).first()
  if version:
   score,covered=_score(version,skill_names);options.append((score,item.created_at,item,version,covered))
 options.sort(key=lambda x:(x[0],x[1]),reverse=True)
 resume=options[0][2] if options else None
 if not resume:raise HTTPException(404,'No eligible candidate-owned resume found')
 score,_,_,version,covered=options[0];value=db.query(ResumeSelection).filter(ResumeSelection.candidate_id==candidate_id,ResumeSelection.job_id==job_id).first()
 evidence={'formula':'10 points per canonical JD skill found in parsed resume text + 5 parsed-structure points; newest resume breaks ties','covered_skills':covered,'score':score}
 if not value:value=ResumeSelection(candidate_id=candidate_id,job_id=job_id,resume_id=resume.id,resume_version_id=version.id,selection_method='manual' if resume_id else 'ranked',selection_score=score,selection_evidence=evidence,explanation='Selected from parsed candidate-owned resumes using deterministic skill coverage and completeness; no resume content was changed.');db.add(value)
 else:value.resume_id=resume.id;value.resume_version_id=version.id;value.selection_score=score;value.selection_evidence=evidence
 db.commit();db.refresh(value);return value
