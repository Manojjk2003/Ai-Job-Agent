import re
from datetime import datetime,timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.job import Job,JobSource
VERSION='1'
def normalize_title(value):return re.sub(r'\s+',' ',value or '').strip()
def normalize_location(value):return re.sub(r'\s+',' ',(value or '').strip().lower()).replace('bangalore','bengaluru')
def normalize_source(db:Session,source_id):
 source=db.get(JobSource,source_id)
 if not source:raise HTTPException(404,'Job source not found')
 if not source.source_title:source.normalization_status='failed';source.normalization_error='Source title is required';db.commit();raise HTTPException(422,source.normalization_error)
 job=db.get(Job,source.job_id);job.canonical_title=normalize_title(source.source_title);job.normalized_title=job.canonical_title.lower();job.description=source.source_description or job.description;now=datetime.now(timezone.utc);job.normalization_version=VERSION;job.normalized_at=now;source.normalization_status='completed';source.normalization_version=VERSION;source.normalized_at=now;source.normalization_error=None;db.commit();db.refresh(job);return job
