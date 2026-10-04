import hashlib,re
from datetime import datetime,timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.job import Job
from app.db.models.job_analysis import JobAnalysis,JobRequirement,JobSkill
from app.db.models.skill import Skill,SkillAlias
from app.providers.llm import GeminiJDAnalysisProvider, JDAnalysisProvider, LLMProviderError
from app.schemas.jd_analysis import JDAnalysisOutput
from app.core.config import settings
VERSION='1.0'
def _importance(text,pos):
 before=text[max(0,pos-120):pos].lower()
 return 'preferred' if any(x in before for x in ('preferred','nice to have','bonus')) else 'required' if any(x in before for x in ('required','must','need')) else 'unknown'
def _persist_output(db, job, analysis, output: JDAnalysisOutput, content: str):
 for item in output.requirements:
  evidence=' '.join(item.evidence.split())
  if evidence.lower() not in content.lower():
   analysis.status='needs_review'
   continue
  req=JobRequirement(analysis_id=analysis.id,job_id=job.id,requirement_type=item.requirement_type,importance=item.importance,description=item.description,normalized_text=' '.join(item.description.lower().split()),evidence_text=evidence,source_section=None,confidence=item.confidence);db.add(req);db.flush()
  if item.requirement_type=='skill':
   skill=db.scalar(select(Skill).where(Skill.normalized_name==req.normalized_text)) or db.scalar(select(Skill).join(SkillAlias,SkillAlias.skill_id==Skill.id).where(SkillAlias.normalized_alias==req.normalized_text))
   if skill:db.add(JobSkill(analysis_id=analysis.id,job_id=job.id,skill_id=skill.id,importance=item.importance,evidence_text=evidence,confidence=item.confidence,source_requirement_id=req.id))

def analyze(db:Session,job_id,provider:JDAnalysisProvider|None=None):
 job=db.get(Job,job_id)
 if not job:raise HTTPException(404,'Job not found')
 content=(job.description or '')[:20000]
 if not content:raise HTTPException(422,'Job description is required for analysis')
 digest=hashlib.sha256((job.canonical_title+'\n'+content).encode()).hexdigest();existing=db.scalar(select(JobAnalysis).where(JobAnalysis.job_id==job.id,JobAnalysis.source_content_hash==digest,JobAnalysis.analysis_version==VERSION,JobAnalysis.status=='completed'))
 if existing:return existing
 analysis=JobAnalysis(job_id=job.id,status='analyzing',analysis_version=VERSION,model_provider=(provider.name if provider else 'gemini'),model_name=settings.gemini_model if provider is None else None,prompt_version=VERSION,source_content_hash=digest);db.add(analysis);db.flush()
 provider=provider or GeminiJDAnalysisProvider()
 try:
  output=provider.analyze_jd(title=job.canonical_title,description=content)
  _persist_output(db,job,analysis,output,content)
 except LLMProviderError as exc:
  analysis.status='failed';analysis.error_message='JD analysis provider is unavailable or returned invalid output';db.commit();raise HTTPException(503,analysis.error_message) from exc
 except Exception:
  analysis.status='failed';analysis.error_message='JD analysis could not be completed';db.commit();raise
 analysis.raw_response_hash=hashlib.sha256(output.model_dump_json().encode()).hexdigest()
 if analysis.status=='analyzing':analysis.status='completed'
 analysis.analyzed_at=datetime.now(timezone.utc);db.commit();db.refresh(analysis);return analysis
