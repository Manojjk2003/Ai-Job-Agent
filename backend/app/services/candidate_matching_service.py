from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.candidate_job_match import CandidateJobMatch,CandidateJobMatchEvidence
from app.db.models.job import Job
from app.db.models.job_analysis import JobAnalysis,JobRequirement,JobSkill
from app.db.models.skill import CandidateSkill
VERSION='1.0'
def match(db:Session,candidate_id,job_id):
 if not db.get(Job,job_id):raise HTTPException(404,'Job not found')
 analysis=db.query(JobAnalysis).filter(JobAnalysis.job_id==job_id,JobAnalysis.status=='completed').order_by(JobAnalysis.created_at.desc()).first()
 if not analysis:raise HTTPException(409,'Job requires completed JD analysis')
 value=db.query(CandidateJobMatch).filter(CandidateJobMatch.candidate_id==candidate_id,CandidateJobMatch.job_id==job_id).first()
 if not value:value=CandidateJobMatch(candidate_id=candidate_id,job_id=job_id,status='completed',match_version=VERSION);db.add(value);db.flush()
 else:db.query(CandidateJobMatchEvidence).filter(CandidateJobMatchEvidence.match_id==value.id).delete()
 skills={x.skill_id:x for x in db.query(CandidateSkill).filter(CandidateSkill.candidate_id==candidate_id).all()}
 for item in db.query(JobSkill).filter(JobSkill.analysis_id==analysis.id).all():
  req=db.get(JobRequirement,item.source_requirement_id);candidate_skill=skills.get(item.skill_id);classification='strong_match' if candidate_skill else 'missing';reason='Verified candidate skill matches this JD requirement' if candidate_skill else 'No verified candidate skill evidence exists for this requirement';db.add(CandidateJobMatchEvidence(match_id=value.id,job_requirement_id=req.id if req else None,candidate_skill_id=candidate_skill.id if candidate_skill else None,classification=classification,reason=reason))
 db.commit();return value
