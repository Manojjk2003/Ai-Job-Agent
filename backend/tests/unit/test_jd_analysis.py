from app.services.jd_analysis_service import _importance
from app.providers.llm import GeminiJDAnalysisProvider, LLMProviderError, StaticJDAnalysisProvider
from app.schemas.jd_analysis import JDAnalysisOutput, ExtractedRequirement
from app.core.config import settings
def test_jd_importance_is_deterministic():assert _importance('Required: React',10)=='required' and _importance('Preferred: AWS',11)=='preferred'
def test_static_provider_returns_pydantic_validated_output():
 output=JDAnalysisOutput(requirements=[ExtractedRequirement(requirement_type='education',description='Bachelor degree',importance='required',evidence='Bachelor degree required')])
 assert StaticJDAnalysisProvider(output).analyze_jd(title='Engineer',description='Bachelor degree required')==output
def test_gemini_provider_fails_safely_when_unconfigured(monkeypatch):
 monkeypatch.setattr(settings,'gemini_api_key',None);monkeypatch.setattr(settings,'gemini_model',None)
 try:GeminiJDAnalysisProvider().analyze_jd(title='Engineer',description='text')
 except LLMProviderError:return
 raise AssertionError('Unconfigured Gemini must not make a request')
