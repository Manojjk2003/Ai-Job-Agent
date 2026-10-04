from typing import Literal
from pydantic import BaseModel, Field

Importance = Literal['required', 'preferred', 'nice_to_have', 'unknown']
RequirementType = Literal['skill', 'experience', 'education', 'certification', 'responsibility', 'qualification', 'language', 'domain_knowledge', 'other']

class ExtractedRequirement(BaseModel):
    requirement_type: RequirementType
    description: str = Field(min_length=1, max_length=2000)
    importance: Importance = 'unknown'
    evidence: str = Field(min_length=1, max_length=4000)
    confidence: Literal['low', 'medium', 'high'] = 'medium'

class JDAnalysisOutput(BaseModel):
    requirements: list[ExtractedRequirement] = Field(default_factory=list, max_length=100)
