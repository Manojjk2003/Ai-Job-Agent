import uuid
from datetime import datetime
from pydantic import BaseModel,ConfigDict
class ResumeVersionResponse(BaseModel):
 id:uuid.UUID;resume_id:uuid.UUID;version_number:int;parse_status:str;parser_name:str|None;parser_version:str|None;structured_sections:dict|None;error_message:str|None;parsed_at:datetime|None;created_at:datetime
 model_config=ConfigDict(from_attributes=True)
