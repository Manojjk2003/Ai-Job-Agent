from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.models.skill import Skill,CandidateSkill,SkillEvidence
from app.repositories import skill_repository as repo
SEEDS=[('JavaScript','Programming Language'),('TypeScript','Programming Language'),('Python','Programming Language'),('Java','Programming Language'),('C#','Programming Language'),('C++','Programming Language'),('HTML','Frontend'),('CSS','Frontend'),('Angular','Framework'),('React','Library'),('Vue','Framework'),('Node.js','Backend'),('FastAPI','Framework'),('Express','Framework'),('Django','Framework'),('Spring Boot','Framework'),('MySQL','Database'),('PostgreSQL','Database'),('MongoDB','Database'),('Firebase','Cloud'),('AWS','Cloud'),('Docker','DevOps'),('Git','Tools'),('GitHub','Tools'),('REST API','Architecture'),('GraphQL','Architecture'),('Redis','Database'),('Kubernetes','DevOps')]
def norm(v): return ' '.join(v.strip().lower().split())
def seed(db):
 for name,cat in SEEDS:
  if not db.scalar(select(Skill).where(Skill.normalized_name==norm(name))): db.add(Skill(name=name,normalized_name=norm(name),category=cat))
 db.commit()
def add(db,cid,data):
 if not db.get(Skill,data['skill_id']): raise HTTPException(404,'Skill not found')
 x=CandidateSkill(candidate_id=cid,**data);db.add(x)
 try: db.commit()
 except IntegrityError: db.rollback();raise HTTPException(409,'Candidate already has this skill')
 db.refresh(x);return x
def get(db,cid,id):
 x=repo.owned(db,id,cid)
 if not x: raise HTTPException(404,'Candidate skill not found')
 return x
def update(db,cid,id,data):
 x=get(db,cid,id)
 for k,v in data.items():setattr(x,k,v)
 db.commit();db.refresh(x);return x
def delete(db,cid,id):db.delete(get(db,cid,id));db.commit()
def evidence_list(db,cid,skill_id): return repo.evidence_list(db,get(db,cid,skill_id).id)
def evidence_get(db,cid,skill_id,evidence_id):
 x=repo.evidence_get(db,evidence_id,get(db,cid,skill_id).id)
 if not x: raise HTTPException(404,'Skill evidence not found')
 return x
def evidence_create(db,cid,skill_id,data):
 x=SkillEvidence(candidate_skill_id=get(db,cid,skill_id).id,**data);db.add(x);db.commit();db.refresh(x);return x
def evidence_update(db,cid,skill_id,evidence_id,data):
 x=evidence_get(db,cid,skill_id,evidence_id)
 for k,v in data.items():setattr(x,k,v)
 db.commit();db.refresh(x);return x
def evidence_delete(db,cid,skill_id,evidence_id):db.delete(evidence_get(db,cid,skill_id,evidence_id));db.commit()
