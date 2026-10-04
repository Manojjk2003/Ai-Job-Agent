from datetime import datetime,timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.job import Job,JobSource,JobLocation
from app.db.models.hiring_source import CompanyHiringSource
def title(v):return ' '.join(v.split())
def url(v):return v.rstrip('/')
def add(db:Session,item):
 source=db.get(CompanyHiringSource,item.company_hiring_source_id)
 if not source or source.company_id!=item.company_id:raise HTTPException(422,'Hiring source does not belong to company')
 existing=db.query(JobSource).filter(JobSource.company_hiring_source_id==item.company_hiring_source_id,JobSource.normalized_source_url==url(item.source_url)).first()
 if existing:return db.get(Job,existing.job_id)
 now=datetime.now(timezone.utc);job=Job(company_id=item.company_id,canonical_title=title(item.title),normalized_title=title(item.title).lower(),description=item.description,employment_type=item.employment_type,workplace_mode=item.workplace_mode,application_url=item.application_url,first_seen_at=now,last_seen_at=now);db.add(job);db.flush();db.add(JobSource(job_id=job.id,company_hiring_source_id=item.company_hiring_source_id,external_job_id=item.external_job_id,source_url=item.source_url,normalized_source_url=url(item.source_url),source_title=item.title,source_description=item.description,status='open',first_seen_at=now,last_seen_at=now));
 if item.location_name:db.add(JobLocation(job_id=job.id,location_name=item.location_name,normalized_location=item.location_name.strip().lower(),city=item.city))
 db.commit();db.refresh(job);return job
