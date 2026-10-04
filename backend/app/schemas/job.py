import uuid
from pydantic import BaseModel,ConfigDict,Field
class JobWrite(BaseModel):company_id:uuid.UUID;company_hiring_source_id:uuid.UUID;title:str=Field(min_length=1,max_length=500);source_url:str=Field(min_length=8,max_length=2048);external_job_id:str|None=Field(None,max_length=255);description:str|None=Field(None,max_length=50000);location_name:str|None=Field(None,max_length=255);city:str|None=Field(None,max_length=255);employment_type:str|None=Field(None,max_length=50);workplace_mode:str|None=Field(None,max_length=50);application_url:str|None=Field(None,max_length=2048)
class JobResponse(BaseModel):id:uuid.UUID;company_id:uuid.UUID;canonical_title:str;normalized_title:str;description:str|None;status:str;application_url:str|None;model_config=ConfigDict(from_attributes=True)
class JobDiscoveryRequest(BaseModel):jobs:list[JobWrite]=Field(default_factory=list,max_length=100)
