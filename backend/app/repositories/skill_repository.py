from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.db.models.skill import Skill,SkillAlias,CandidateSkill,SkillEvidence
def search(db:Session,q:str|None):
 s=select(Skill).where(Skill.is_active)
 if q: s=s.outerjoin(SkillAlias).where(or_(Skill.normalized_name.contains(q),SkillAlias.normalized_alias.contains(q)))
 return list(db.scalars(s.distinct().order_by(Skill.name)))
def candidate_list(db,cid): return list(db.scalars(select(CandidateSkill).where(CandidateSkill.candidate_id==cid)))
def owned(db,id,cid): return db.scalar(select(CandidateSkill).where(CandidateSkill.id==id,CandidateSkill.candidate_id==cid))
def evidence_list(db,candidate_skill_id): return list(db.scalars(select(SkillEvidence).where(SkillEvidence.candidate_skill_id==candidate_skill_id)))
def evidence_get(db,id,candidate_skill_id): return db.scalar(select(SkillEvidence).where(SkillEvidence.id==id,SkillEvidence.candidate_skill_id==candidate_skill_id))
