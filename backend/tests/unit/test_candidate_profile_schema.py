import pytest
from pydantic import ValidationError

from app.schemas.candidate_profile import CandidateProfileCreate


def test_profile_schema_rejects_negative_experience() -> None:
    with pytest.raises(ValidationError):
        CandidateProfileCreate(years_experience=-1)


def test_profile_schema_accepts_valid_candidate_facts() -> None:
    profile = CandidateProfileCreate(location="Bengaluru", years_experience=2)
    assert profile.location == "Bengaluru"
    assert profile.years_experience == 2
