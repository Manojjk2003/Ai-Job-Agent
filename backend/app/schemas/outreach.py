import uuid
from typing import Literal
from urllib.parse import urlparse
from pydantic import BaseModel,Field,field_validator
ContactType=Literal['recruiter','talent_acquisition','hiring_manager','hr','founder','team_lead','employee_referral','general_hiring_contact','company_contact','other']
class ContactWrite(BaseModel):
 name:str=Field(min_length=1,max_length=255);job_title:str|None=Field(None,max_length=255);email:str|None=Field(None,max_length=255);phone:str|None=Field(None,max_length=50);profile_url:str|None=Field(None,max_length=2048);source:Literal['user_provided','official_company_site','public_profile','permitted_provider','company_job_posting','referral','other']='user_provided';source_url:str|None=Field(None,max_length=2048);contact_type:ContactType='other';is_public:bool=False;notes:str|None=Field(None,max_length=5000)
 @field_validator('profile_url','source_url')
 @classmethod
 def valid_url(cls,v):
  if v is None:return v
  p=urlparse(v)
  if p.scheme not in {'http','https'} or not p.hostname:raise ValueError('URL must be absolute HTTP(S)')
  return v
class OutreachWrite(BaseModel):contact_id:uuid.UUID|None=None;channel:Literal['email','linkedin','company_contact_form','other_permitted_channel']='email';subject:str=Field(min_length=1,max_length=500);body:str=Field(min_length=1,max_length=10000);call_to_action:str|None=Field(None,max_length=500)
