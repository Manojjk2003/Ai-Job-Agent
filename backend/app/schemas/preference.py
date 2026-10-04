from pydantic import BaseModel, Field, model_validator

class PreferenceWrite(BaseModel):
    job_search_active: bool = False
    work_modes: list[str] = []
    employment_types: list[str] = []
    target_seniority: list[str] = []
    min_experience_years: int | None = Field(None, ge=0)
    max_experience_years: int | None = Field(None, ge=0)
    min_salary: int | None = Field(None, ge=0)
    max_salary: int | None = Field(None, ge=0)
    salary_currency: str | None = None
    salary_period: str | None = None
    relocation_preference: str | None = None
    company_preferences: list[str] = []

    @model_validator(mode='after')
    def ranges(self):
        if self.min_experience_years is not None and self.max_experience_years is not None and self.min_experience_years > self.max_experience_years:
            raise ValueError('Invalid experience range')
        if self.min_salary is not None and self.max_salary is not None and self.min_salary > self.max_salary:
            raise ValueError('Invalid salary range')
        return self
