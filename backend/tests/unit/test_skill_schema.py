import pytest
from pydantic import ValidationError
from app.schemas.skill import CandidateSkillCreate
def test_invalid_proficiency():
 with pytest.raises(ValidationError):CandidateSkillCreate(skill_id='00000000-0000-0000-0000-000000000000',proficiency='wrong')
def test_negative_years():
 with pytest.raises(ValidationError):CandidateSkillCreate(skill_id='00000000-0000-0000-0000-000000000000',years_experience=-1)
