import uuid
from pydantic import BaseModel,ConfigDict,Field
class RoleProfileWrite(BaseModel):name:str=Field(max_length=255);target_designation:str=Field(max_length=255);headline:str|None=Field(None,max_length=255);summary:str|None=Field(None,max_length=10000);target_seniority:str|None=None;is_active:bool=True
class RoleProfileCreate(RoleProfileWrite):is_default:bool=False
class RoleProfileResponse(RoleProfileWrite):id:uuid.UUID;candidate_id:uuid.UUID;is_default:bool;model_config=ConfigDict(from_attributes=True)
class RoleProfileLink(BaseModel):priority:int=Field(ge=1);is_primary:bool=False
