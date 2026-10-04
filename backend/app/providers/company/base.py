from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProviderLocation:
    location_name: str
    area: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    location_type: str = "unknown"
    is_headquarters: bool = False


@dataclass(frozen=True)
class ProviderCompanyResult:
    name: str
    external_id: str | None = None
    website_url: str | None = None
    legal_name: str | None = None
    linkedin_url: str | None = None
    description: str | None = None
    industry: str | None = None
    company_size: str | None = None
    company_stage: str | None = None
    logo_url: str | None = None
    status: str = "unknown"
    locations: list[ProviderLocation] = field(default_factory=list)


class CompanyDiscoveryProvider(ABC):
    name: str

    @abstractmethod
    def search_companies(self, *, location: ProviderLocation, companies: list[ProviderCompanyResult], max_results: int) -> list[ProviderCompanyResult]:
        """Return provider-independent company facts; no database writes occur here."""

    def get_company(self, external_id: str) -> ProviderCompanyResult | None:
        return None

    def health_check(self) -> bool:
        return True
