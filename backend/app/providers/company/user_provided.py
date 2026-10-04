from app.providers.company.base import CompanyDiscoveryProvider, ProviderCompanyResult, ProviderLocation


class UserProvidedCompanyProvider(CompanyDiscoveryProvider):
    """A deterministic provider for facts explicitly submitted by an authenticated user."""

    name = "user_provided"

    def search_companies(self, *, location: ProviderLocation, companies: list[ProviderCompanyResult], max_results: int) -> list[ProviderCompanyResult]:
        return companies[:max_results]
