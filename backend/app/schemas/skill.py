import uuid
from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field
class Proficiency(StrEnum): beginner='beginner'; intermediate='intermediate'; advanced='advanced'; expert='expert'
class EvidenceType(StrEnum): experience='experience'; project='project'; education='education'; certification='certification'; candidate_claim='candidate_claim'
class SkillResponse(BaseModel): id:uuid.UUID; name:str; category:str; model_config=ConfigDict(from_attributes=True)
class CandidateSkillWrite(BaseModel): skill_id:uuid.UUID; proficiency:Proficiency|None=None; years_experience:int|None=Field(None,ge=0,le=80); is_primary:bool=False
class CandidateSkillCreate(CandidateSkillWrite): pass
class CandidateSkillUpdate(CandidateSkillWrite): pass
class CandidateSkillResponse(CandidateSkillWrite): id:uuid.UUID; candidate_id:uuid.UUID; model_config=ConfigDict(from_attributes=True)
class SkillEvidenceCreate(BaseModel): evidence_type:EvidenceType; reference_id:uuid.UUID|None=None; description:str|None=Field(None,max_length=5000)
class SkillEvidenceUpdate(SkillEvidenceCreate): pass
class SkillEvidenceResponse(SkillEvidenceCreate): id:uuid.UUID; candidate_skill_id:uuid.UUID; model_config=ConfigDict(from_attributes=True)
