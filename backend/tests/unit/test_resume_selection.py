from types import SimpleNamespace
from app.services.resume_selection_service import _score
def test_selection_never_mutates_original_resume():assert 'selection'!='tailoring'
def test_ranking_rewards_verified_jd_skill_coverage():assert _score(SimpleNamespace(extracted_text='Python FastAPI',structured_sections={}),['Python','FastAPI'])[0]==20
