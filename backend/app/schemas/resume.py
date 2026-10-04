import uuid
from datetime import datetime
from pydantic import BaseModel,ConfigDict
class ResumeResponse(BaseModel):
 id:uuid.UUID;original_filename:str;mime_type:str;file_size:int;file_hash:str;status:str;created_at:datetime
 model_config=ConfigDict(from_attributes=True)
