from datetime import datetime,timezone
from urllib.parse import urlparse,urlunparse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.company import Company
from app.db.models.hiring_source import HiringSource,CompanyHiringSource
from app.providers.hiring_source import ProviderHiringSource,UserProvidedHiringSourceProvider
from app.repositories import hiring_source_repository as repo
from app.schemas.hiring_source import HiringSourceWrite
def normalize_url(url):
 p=urlparse(url);path=p.path.rstrip('/') or '/';return urlunparse((p.scheme.lower(),p.netloc.lower().removeprefix('www.'),path,'',p.query,''))
def normalize_name(name):return ' '.join(name.lower().split())
def classify(item):
 host=(urlparse(item.source_url).hostname or '').lower()
 if item.source_type=='official_careers' and host: return item.source_type
 return item.source_type
def company(db,id):
 value=db.get(Company,id)
 if not value:raise HTTPException(404,'Company not found')
 return value
def upsert(db,company_id,item,method='user_provided'):
 normalized_name=normalize_name(item.name);typ=classify(item);base=f'{urlparse(item.source_url).scheme}://{urlparse(item.source_url).netloc}'
 source=repo.source(db,normalized_name,typ)
 if not source:source=HiringSource(name=item.name.strip(),normalized_name=normalized_name,source_type=typ,base_url=base);db.add(source);db.flush()
 url=normalize_url(item.source_url);value=repo.link(db,company_id,source.id,url);now=datetime.now(timezone.utc)
 verified=typ=='official_careers' and company(db,company_id).website_domain==(urlparse(url).hostname or '').removeprefix('www.')
 if not value:value=CompanyHiringSource(company_id=company_id,hiring_source_id=source.id,source_url=item.source_url,normalized_source_url=url,status='verified' if verified else 'discovered',confidence='high' if verified else 'medium',discovery_method=method,last_checked_at=now,last_verified_at=now if verified else None,notes=item.notes,external_reference=item.external_reference);db.add(value)
 else:value.last_checked_at=now;value.last_verified_at=now if verified else value.last_verified_at;value.status='verified' if verified else value.status
 return value
def add(db,company_id,item):
 company(db,company_id);value=upsert(db,company_id,item,'manual');db.commit();db.refresh(value);return value
def discover(db,company_id,items):
 company(db,company_id);provider=UserProvidedHiringSourceProvider();result=[]
 for item in provider.discover_sources([ProviderHiringSource(**x.model_dump()) for x in items]):result.append(upsert(db,company_id,HiringSourceWrite(**item.__dict__)))
 db.commit();return result
