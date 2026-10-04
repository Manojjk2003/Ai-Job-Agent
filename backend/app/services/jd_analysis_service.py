import hashlib,re
from datetime import datetime,timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.job import Job
from app.db.models.job_analysis import JobAnalysis,JobRequirement,JobSkill
from app.db.models.skill import Skill,SkillAlias
VERSION='1.0'
def _importance(text,pos):
 before=text[max(0,pos-120):pos].lower()
 return 'preferred' if any(x in before for x in ('preferred','nice to have','bonus')) else 'required' if any(x in before for x in ('required','must','need')) else 'unknown'
def analyze(db:Session,job_id):
 job=db.get(Job,job_id)
 if not job:raise HTTPException(404,'Job not found')
 content=(job.description or '')[:20000]
 if not content:raise HTTPException(422,'Job description is required for analysis')
 digest=hashlib.sha256((job.canonical_title+'\n'+content).encode()).hexdigest();existing=db.scalar(select(JobAnalysis).where(JobAnalysis.job_id==job.id,JobAnalysis.source_content_hash==digest,JobAnalysis.analysis_version==VERSION,JobAnalysis.status=='completed'))
 if existing:return existing
 analysis=JobAnalysis(job_id=job.id,status='analyzing',analysis_version=VERSION,model_provider='deterministic_local',model_name=None,prompt_version=VERSION,source_content_hash=digest);db.add(analysis);db.flush()
 for skill in db.scalars(select(Skill).where(Skill.is_active==True)):
  aliases=[skill.normalized_name]+list(db.scalars(select(SkillAlias.normalized_alias).where(SkillAlias.skill_id==skill.id)))
  match=next((a for a in aliases if re.search(r'(?<!\w)'+re.escape(a)+r'(?!\w)',content.lower())),None)
  if not match:continue
  pos=content.lower().find(match);evidence=content[max(0,content.rfind('.',0,pos)+1):content.find('.',pos)+1 or len(content)].strip();imp=_importance(content,pos);req=JobRequirement(analysis_id=analysis.id,job_id=job.id,requirement_type='skill',importance=imp,description=skill.name,normalized_text=skill.normalized_name,source_section=None,confidence='high');db.add(req);db.flush();db.add(JobSkill(analysis_id=analysis.id,job_id=job.id,skill_id=skill.id,importance=imp,evidence_text=evidence,confidence='high',source_requirement_id=req.id))
 analysis.status='completed';analysis.analyzed_at=datetime.now(timezone.utc);db.commit();db.refresh(analysis);return analysis
