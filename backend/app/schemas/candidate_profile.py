import uuid

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class CandidateProfileCreate(BaseModel):
    phone: str | None = Field(default=None, max_length=30)
    location: str | None = Field(default=None, max_length=255)
    headline: str | None = Field(default=None, max_length=255)
    summary: str | None = Field(default=None, max_length=10000)
    years_experience: int | None = Field(default=None, ge=0)
    current_designation: str | None = Field(default=None, max_length=255)
    linkedin_url: HttpUrl | None = None
    github_url: HttpUrl | None = None


class CandidateProfileResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    phone: str | None
    location: str | None
    headline: str | None
    summary: str | None
    years_experience: int | None
    current_designation: str | None
    linkedin_url: str | None
    github_url: str | None

    model_config = ConfigDict(from_attributes=True)


class CandidateProfileUpdate(CandidateProfileCreate):
    pass
