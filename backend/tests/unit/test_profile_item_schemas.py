from datetime import date
import pytest
from pydantic import ValidationError
from app.schemas.profile_items import ExperienceCreate, ProjectCreate

def test_current_experience_rejects_end_date():
    with pytest.raises(ValidationError): ExperienceCreate(company_name="Acme", job_title="Developer", start_date=date(2024,1,1), end_date=date(2024,2,1), is_current=True)
def test_experience_rejects_reverse_dates():
    with pytest.raises(ValidationError): ExperienceCreate(company_name="Acme", job_title="Developer", start_date=date(2025,1,1), end_date=date(2024,1,1))
def test_project_rejects_reverse_dates():
    with pytest.raises(ValidationError): ProjectCreate(name="Portfolio", start_date=date(2025,1,1), end_date=date(2024,1,1))
