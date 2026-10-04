from sqlalchemy import select
from app.db.models.resume import Resume
def list_for_candidate(db,cid):return list(db.scalars(select(Resume).where(Resume.candidate_id==cid,Resume.status=='UPLOADED').order_by(Resume.created_at.desc())))
def owned(db,id,cid):return db.scalar(select(Resume).where(Resume.id==id,Resume.candidate_id==cid,Resume.status=='UPLOADED'))
def duplicate(db,cid,hash):return db.scalar(select(Resume).where(Resume.candidate_id==cid,Resume.file_hash==hash,Resume.status=='UPLOADED'))
