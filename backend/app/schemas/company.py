import uuid
from datetime import datetime
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator

Confidence = Literal["low", "medium", "high"]
CompanyStatus = Literal["active", "inactive", "unknown"]
LocationType = Literal["headquarters", "office", "branch", "remote", "unknown"]


class CompanyLocationWrite(BaseModel):
    location_name: str = Field(min_length=1, max_length=255)
    area: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=255)
    state: str | None = Field(None, max_length=255)
    country: str | None = Field(None, max_length=255)
    postal_code: str | None = Field(None, max_length=30)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    location_type: LocationType = "unknown"
    is_headquarters: bool = False


class CompanyLocationResponse(CompanyLocationWrite):
    id: uuid.UUID
    company_id: uuid.UUID
    normalized_location: str
    is_verified: bool
    confidence: Confidence
    source: str
    model_config = ConfigDict(from_attributes=True)


class CompanyWrite(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    legal_name: str | None = Field(None, max_length=255)
    website_url: str | None = Field(None, max_length=2048)
    linkedin_url: str | None = Field(None, max_length=2048)
    description: str | None = Field(None, max_length=10000)
    industry: str | None = Field(None, max_length=255)
    company_size: str | None = Field(None, max_length=100)
    company_stage: str | None = Field(None, max_length=100)
    logo_url: str | None = Field(None, max_length=2048)
    status: CompanyStatus = "unknown"
    locations: list[CompanyLocationWrite] = Field(default_factory=list, max_length=50)

    @field_validator("website_url", "linkedin_url", "logo_url")
    @classmethod
    def valid_url(cls, value: str | None) -> str | None:
        if value is None:
            return value
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("URL must be an absolute HTTP(S) URL")
        return value


class CompanyResponse(BaseModel):
    id: uuid.UUID
    canonical_name: str
    normalized_name: str
    legal_name: str | None
    website_url: str | None
    website_domain: str | None
    linkedin_url: str | None
    description: str | None
    industry: str | None
    company_size: str | None
    company_stage: str | None
    logo_url: str | None
    status: CompanyStatus
    confidence: Confidence
    locations: list[CompanyLocationResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DiscoveryLocation(BaseModel):
    location_name: str | None = Field(None, max_length=255)
    area: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=255)
    state: str | None = Field(None, max_length=255)
    country: str | None = Field(None, max_length=255)


class CompanyDiscoveryRequest(BaseModel):
    location: DiscoveryLocation | None = None
    role_profile_id: uuid.UUID | None = None
    max_results: int = Field(default=25, ge=1, le=100)
    companies: list[CompanyWrite] = Field(default_factory=list, max_length=100)


class CompanyDiscoveryRunResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    role_profile_id: uuid.UUID | None
    query: str | None
    location_name: str
    area: str | None
    city: str | None
    state: str | None
    country: str | None
    provider_name: str
    status: Literal["pending", "running", "completed", "failed", "partial"]
    result_count: int
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CompanyDiscoveryResponse(BaseModel):
    run: CompanyDiscoveryRunResponse
    companies: list[CompanyResponse]
