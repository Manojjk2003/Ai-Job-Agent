from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.hiring_source import HiringSource,CompanyHiringSource
def source(db:Session,name,typ):return db.scalar(select(HiringSource).where(HiringSource.normalized_name==name,HiringSource.source_type==typ))
def link(db:Session,company_id,source_id,url):return db.scalar(select(CompanyHiringSource).where(CompanyHiringSource.company_id==company_id,CompanyHiringSource.hiring_source_id==source_id,CompanyHiringSource.normalized_source_url==url))
def list_for_company(db:Session,company_id):return list(db.scalars(select(CompanyHiringSource).where(CompanyHiringSource.company_id==company_id).order_by(CompanyHiringSource.created_at.desc())))
