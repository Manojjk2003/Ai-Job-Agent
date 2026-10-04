import uuid
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

class _Owned(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class ExperienceWrite(BaseModel):
    company_name: str = Field(max_length=255)
    job_title: str = Field(max_length=255)
    employment_type: str | None = Field(default=None, max_length=80)
    location: str | None = Field(default=None, max_length=255)
    start_date: date
    end_date: date | None = None
    is_current: bool = False
    description: str | None = Field(default=None, max_length=10000)
    display_order: int = Field(default=0, ge=0)
    @model_validator(mode="after")
    def validate_dates(self):
        if self.is_current and self.end_date is not None: raise ValueError("Current experience must not have an end date")
        if not self.is_current and self.end_date is not None and self.start_date > self.end_date: raise ValueError("start_date must be on or before end_date")
        return self
class ExperienceCreate(ExperienceWrite): pass
class ExperienceUpdate(ExperienceWrite): pass
class ExperienceResponse(ExperienceWrite, _Owned): id: uuid.UUID; candidate_id: uuid.UUID

class AchievementWrite(BaseModel):
    achievement: str = Field(min_length=1, max_length=5000)
    display_order: int = Field(default=0, ge=0)
class ExperienceAchievementCreate(AchievementWrite): pass
class ExperienceAchievementUpdate(AchievementWrite): pass
class ExperienceAchievementResponse(AchievementWrite, _Owned): id: uuid.UUID; experience_id: uuid.UUID

class EducationWrite(BaseModel):
    institution: str = Field(max_length=255)
    degree: str | None = Field(default=None, max_length=255)
    field_of_study: str | None = Field(default=None, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    grade: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=10000)
    display_order: int = Field(default=0, ge=0)
    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date: raise ValueError("start_date must be on or before end_date")
        return self
class EducationCreate(EducationWrite): pass
class EducationUpdate(EducationWrite): pass
class EducationResponse(EducationWrite, _Owned): id: uuid.UUID; candidate_id: uuid.UUID

class ProjectWrite(BaseModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=10000)
    role: str | None = Field(default=None, max_length=255)
    project_type: str | None = Field(default=None, max_length=100)
    start_date: date | None = None
    end_date: date | None = None
    project_url: HttpUrl | None = None
    repository_url: HttpUrl | None = None
    display_order: int = Field(default=0, ge=0)
    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date and self.end_date and self.start_date > self.end_date: raise ValueError("start_date must be on or before end_date")
        return self
class ProjectCreate(ProjectWrite): pass
class ProjectUpdate(ProjectWrite): pass
class ProjectResponse(ProjectWrite, _Owned): id: uuid.UUID; candidate_id: uuid.UUID
