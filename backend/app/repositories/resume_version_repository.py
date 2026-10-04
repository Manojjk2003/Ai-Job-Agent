from sqlalchemy import select,func
from app.db.models.resume_version import ResumeVersion
def latest(db,resume_id):return db.scalar(select(ResumeVersion).where(ResumeVersion.resume_id==resume_id).order_by(ResumeVersion.version_number.desc()))
def list_versions(db,resume_id):return list(db.scalars(select(ResumeVersion).where(ResumeVersion.resume_id==resume_id).order_by(ResumeVersion.version_number.desc())))
def get(db,id,resume_id):return db.scalar(select(ResumeVersion).where(ResumeVersion.id==id,ResumeVersion.resume_id==resume_id))
