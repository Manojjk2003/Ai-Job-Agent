from app.providers.company.base import ProviderCompanyResult, ProviderLocation
from app.providers.company.user_provided import UserProvidedCompanyProvider
from app.schemas.company import CompanyWrite
from app.services.company_discovery_service import confidence_for, normalize_domain, normalize_location, normalize_name


def test_company_name_normalization_is_conservative():
    assert normalize_name("Example Technologies Pvt. Ltd.") == "example technologies"
    assert normalize_name("ABC Technologies Labs") == "abc technologies labs"


def test_domain_normalization_removes_scheme_path_and_www():
    assert normalize_domain("https://www.example.com/careers") == "example.com"
    assert normalize_domain(None) is None


def test_location_normalization_handles_bangalore_alias():
    location = ProviderLocation(location_name="HSR Layout, Bangalore", area="HSR Layout", city="Bangalore", country="India")
    assert normalize_location(location) == "hsr layout|bengaluru|india"


def test_confidence_uses_available_evidence_only():
    assert confidence_for(ProviderCompanyResult(name="Example")) == "low"
    assert confidence_for(ProviderCompanyResult(name="Example", website_url="https://example.com")) == "medium"
    assert confidence_for(ProviderCompanyResult(name="Example", website_url="https://example.com", locations=[ProviderLocation(location_name="Bengaluru")])) == "high"


def test_user_provided_provider_returns_only_submitted_facts():
    provider = UserProvidedCompanyProvider()
    submitted = [ProviderCompanyResult(name="One"), ProviderCompanyResult(name="Two")]
    result = provider.search_companies(location=ProviderLocation(location_name="Bengaluru"), companies=submitted, max_results=1)
    assert result == [ProviderCompanyResult(name="One")]


def test_company_schema_rejects_non_http_website_url():
    try:
        CompanyWrite(name="Example", website_url="javascript:alert(1)")
    except ValueError:
        return
    raise AssertionError("non-HTTP URL should be rejected")
