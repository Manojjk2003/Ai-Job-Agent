import pytest
from pydantic import ValidationError
from app.schemas.skill import SkillEvidenceCreate
def test_invalid_evidence_type_is_rejected():
 with pytest.raises(ValidationError):SkillEvidenceCreate(evidence_type='invented')
def test_evidence_description_limit():
 with pytest.raises(ValidationError):SkillEvidenceCreate(evidence_type='candidate_claim',description='x'*5001)
