import uuid
from datetime import datetime
from typing import Literal
from urllib.parse import urlparse
from pydantic import BaseModel,ConfigDict,Field,field_validator
SourceType=Literal['official_careers','company_website','job_board','professional_network','startup_job_board','aggregator','user_provided','other']
SourceStatus=Literal['discovered','verified','inactive','unavailable','unknown']
class HiringSourceWrite(BaseModel):
 name:str=Field(min_length=1,max_length=255);source_type:SourceType;source_url:str=Field(max_length=2048);external_reference:str|None=Field(None,max_length=255);notes:str|None=Field(None,max_length=5000)
 @field_validator('source_url')
 @classmethod
 def url(cls,v):
  p=urlparse(v)
  if p.scheme not in {'http','https'} or not p.hostname:raise ValueError('source_url must be an absolute HTTP(S) URL')
  return v
class CompanyHiringSourceResponse(BaseModel):
 id:uuid.UUID;company_id:uuid.UUID;hiring_source_id:uuid.UUID;source_url:str;normalized_source_url:str;status:SourceStatus;confidence:Literal['low','medium','high'];discovery_method:str;last_verified_at:datetime|None;last_checked_at:datetime|None;notes:str|None;model_config=ConfigDict(from_attributes=True)
class HiringSourceDiscoveryRequest(BaseModel):sources:list[HiringSourceWrite]=Field(default_factory=list,max_length=50)
class HiringSourceDiscoveryResponse(BaseModel):company_id:uuid.UUID;status:Literal['completed','failed','partial','unavailable'];sources:list[CompanyHiringSourceResponse]
