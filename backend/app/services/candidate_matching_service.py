from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.candidate_job_match import CandidateJobMatch,CandidateJobMatchEvidence
from app.db.models.job import Job
from app.db.models.job_analysis import JobAnalysis,JobRequirement,JobSkill
from app.db.models.skill import CandidateSkill
from app.db.models.candidate_profile import CandidateProfile
from app.db.models.education import Education
from app.db.models.preference import CandidatePreference
from app.db.models.role_profile import RoleProfile
import json,re
VERSION='1.0'
def _classification(actual, required):
 return 'strong_match' if actual is not None and actual >= required else 'partial_match' if actual is not None else 'missing'
def _contains(value, terms):return bool(value and any(term.lower() in value.lower() for term in terms))
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
 profile=db.query(CandidateProfile).filter(CandidateProfile.candidate_id==candidate_id).first()
 preferences=db.query(CandidatePreference).filter(CandidatePreference.candidate_id==candidate_id).first()
 role=db.query(RoleProfile).filter(RoleProfile.candidate_id==candidate_id,RoleProfile.is_default==True,RoleProfile.is_active==True).first()
 for req in db.query(JobRequirement).filter(JobRequirement.analysis_id==analysis.id).all():
  if req.requirement_type=='skill':continue
  if req.requirement_type=='experience':
   years=int(re.search(r'\d+',req.description).group()) if re.search(r'\d+',req.description) else None; status=_classification(profile.years_experience if profile else None,years) if years is not None else 'partial_match';reason=f'Candidate profile records {profile.years_experience if profile and profile.years_experience is not None else "no"} years; requirement is {req.description}'
  elif req.requirement_type=='education':
   education=db.query(Education).filter(Education.candidate_id==candidate_id).all();status='strong_match' if any(_contains((x.degree or '')+' '+x.institution,[req.description]) for x in education) else 'missing';reason='Candidate education records were checked against the explicit JD education requirement'
  else:status='partial_match';reason='Requirement is retained for review; no unverified candidate claim was inferred'
  db.add(CandidateJobMatchEvidence(match_id=value.id,job_requirement_id=req.id,candidate_skill_id=None,classification=status,reason=reason))
 if role and _contains(job.canonical_title,[role.target_designation]):db.add(CandidateJobMatchEvidence(match_id=value.id,job_requirement_id=None,candidate_skill_id=None,classification='strong_match',reason='Default role profile target designation aligns with the job title'))
 if job.workplace_mode:
  modes=json.loads(preferences.work_modes) if preferences and preferences.work_modes else [];status='strong_match' if job.workplace_mode in modes else 'partial_match';db.add(CandidateJobMatchEvidence(match_id=value.id,job_requirement_id=None,candidate_skill_id=None,classification=status,reason='Candidate work-mode preferences were compared without changing eligibility'))
 db.commit();return value
