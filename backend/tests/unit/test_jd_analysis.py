from app.services.jd_analysis_service import _importance
def test_jd_importance_is_deterministic():assert _importance('Required: React',10)=='required' and _importance('Preferred: AWS',11)=='preferred'
