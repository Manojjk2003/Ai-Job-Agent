import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.company import Company, CompanyDiscoveryRun, CompanyDiscoveryRunResult, CompanyLocation
from app.db.models.preference import CandidatePreference, PreferenceLocation
from app.db.models.role_profile import RoleProfile
from app.providers.company.base import ProviderCompanyResult, ProviderLocation
from app.providers.company.user_provided import UserProvidedCompanyProvider
from app.repositories import company_discovery_repository as runs
from app.repositories import company_repository as companies
from app.schemas.company import CompanyDiscoveryRequest, CompanyLocationWrite, CompanyWrite, DiscoveryLocation

_CONFIDENCE = {"low": 1, "medium": 2, "high": 3}


def normalize_name(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    parts = value.split()
    while len(parts) > 1 and parts[-1] in {"pvt", "private", "ltd", "limited", "llp", "inc", "corp", "corporation"}:
        parts.pop()
    return " ".join(parts)


def normalize_domain(url: str | None) -> str | None:
    if not url:
        return None
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host or None


def normalize_location(location: ProviderLocation | CompanyLocationWrite | DiscoveryLocation) -> str:
    values = [getattr(location, key, None) for key in ("area", "city", "state", "country")]
    values = [re.sub(r"\s+", " ", value.strip().lower()) for value in values if value and value.strip()]
    values = ["bengaluru" if value == "bangalore" else value for value in values]
    fallback = getattr(location, "location_name", None)
    return "|".join(values) or re.sub(r"\s+", " ", (fallback or "").strip().lower())


def confidence_for(result: ProviderCompanyResult) -> str:
    if result.website_url and result.locations:
        return "high"
    if result.website_url or result.locations:
        return "medium"
    return "low"


def _location_name(location: ProviderLocation | CompanyLocationWrite | DiscoveryLocation) -> str:
    return getattr(location, "location_name", None) or ", ".join(
        value for value in (getattr(location, "area", None), getattr(location, "city", None), getattr(location, "state", None), getattr(location, "country", None)) if value
    )


def _merge_missing(company: Company, result: ProviderCompanyResult, confidence: str) -> None:
    fields = ("legal_name", "website_url", "linkedin_url", "description", "industry", "company_size", "company_stage", "logo_url")
    for field in fields:
        value = getattr(result, field)
        if value and not getattr(company, field):
            setattr(company, field, value)
    if _CONFIDENCE[confidence] > _CONFIDENCE[company.confidence]:
        company.confidence = confidence


def upsert_from_result(db: Session, result: ProviderCompanyResult, *, source: str = "user_provided") -> Company:
    normalized_name = normalize_name(result.name)
    domain = normalize_domain(result.website_url)
    company = companies.by_domain(db, domain) or companies.by_normalized_name(db, normalized_name)
    confidence = confidence_for(result)
    if company is None:
        company = Company(canonical_name=result.name.strip(), normalized_name=normalized_name, website_domain=domain, website_url=result.website_url, legal_name=result.legal_name, linkedin_url=result.linkedin_url, description=result.description, industry=result.industry, company_size=result.company_size, company_stage=result.company_stage, logo_url=result.logo_url, status=result.status, confidence=confidence)
        db.add(company)
        db.flush()
    else:
        _merge_missing(company, result, confidence)
    for location in result.locations:
        normalized_location = normalize_location(location)
        if not normalized_location:
            continue
        current = companies.location_by_normalized_name(db, company.id, normalized_location)
        if current is None:
            current = CompanyLocation(company_id=company.id, location_name=_location_name(location), normalized_location=normalized_location, area=location.area, city=location.city, state=location.state, country=location.country, location_type=location.location_type, is_headquarters=location.is_headquarters, confidence=confidence, source=source)
            db.add(current)
            db.flush()
            if current.is_headquarters and not company.headquarters_location_id:
                company.headquarters_location_id = current.id
    return company


def _provider_result(item: CompanyWrite) -> ProviderCompanyResult:
    locations = [ProviderLocation(location_name=_location_name(location), area=location.area, city=location.city, state=location.state, country=location.country, location_type=location.location_type, is_headquarters=location.is_headquarters) for location in item.locations]
    return ProviderCompanyResult(name=item.name, website_url=item.website_url, legal_name=item.legal_name, linkedin_url=item.linkedin_url, description=item.description, industry=item.industry, company_size=item.company_size, company_stage=item.company_stage, logo_url=item.logo_url, status=item.status, locations=locations)


def create_manual_company(db: Session, item: CompanyWrite) -> Company:
    company = upsert_from_result(db, _provider_result(item))
    db.commit()
    return companies.by_id(db, company.id)


def update_manual_company(db: Session, company_id, item: CompanyWrite) -> Company:
    existing = companies.by_id(db, company_id)
    if not existing:
        raise HTTPException(404, "Company not found")
    candidate = _provider_result(item)
    domain = normalize_domain(candidate.website_url)
    other = companies.by_domain(db, domain)
    if other and other.id != existing.id:
        raise HTTPException(409, "Website domain belongs to another canonical company")
    existing.canonical_name = candidate.name.strip()
    existing.normalized_name = normalize_name(candidate.name)
    existing.website_url = candidate.website_url
    existing.website_domain = domain
    for field in ("legal_name", "linkedin_url", "description", "industry", "company_size", "company_stage", "logo_url", "status"):
        setattr(existing, field, getattr(candidate, field))
    for location in candidate.locations:
        upsert_from_result(db, ProviderCompanyResult(name=existing.canonical_name, locations=[location]))
    db.commit()
    return companies.by_id(db, existing.id)


def add_location(db: Session, company_id, location: CompanyLocationWrite) -> CompanyLocation:
    company = companies.by_id(db, company_id)
    if not company:
        raise HTTPException(404, "Company not found")
    normalized = normalize_location(location)
    existing = companies.location_by_normalized_name(db, company_id, normalized)
    if existing:
        return existing
    value = CompanyLocation(company_id=company_id, location_name=_location_name(location), normalized_location=normalized, area=location.area, city=location.city, state=location.state, country=location.country, postal_code=location.postal_code, latitude=location.latitude, longitude=location.longitude, location_type=location.location_type, is_headquarters=location.is_headquarters, confidence="medium", source="user_provided")
    db.add(value)
    db.flush()
    if value.is_headquarters:
        company.headquarters_location_id = value.id
    db.commit()
    db.refresh(value)
    return value


def _resolve_location(db: Session, candidate_id, requested: DiscoveryLocation | None) -> ProviderLocation:
    if requested and _location_name(requested):
        return ProviderLocation(location_name=_location_name(requested), area=requested.area, city=requested.city, state=requested.state, country=requested.country)
    preference = db.query(CandidatePreference).filter(CandidatePreference.candidate_id == candidate_id).first()
    if preference:
        preferred = db.query(PreferenceLocation).filter(PreferenceLocation.candidate_preference_id == preference.id).order_by(PreferenceLocation.is_primary.desc()).first()
        if preferred:
            return ProviderLocation(location_name=preferred.display_name)
    raise HTTPException(422, "A discovery location is required when no preferred location is configured")


def discover(db: Session, candidate, request: CompanyDiscoveryRequest):
    location = _resolve_location(db, candidate.id, request.location)
    if request.role_profile_id:
        role_profile = db.query(RoleProfile).filter(RoleProfile.id == request.role_profile_id, RoleProfile.candidate_id == candidate.id).first()
        if not role_profile:
            raise HTTPException(404, "Role profile not found")
    run = CompanyDiscoveryRun(candidate_id=candidate.id, role_profile_id=request.role_profile_id, query=location.location_name, location_name=location.location_name, area=location.area, city=location.city, state=location.state, country=location.country, provider_name="user_provided", status="running", started_at=datetime.now(timezone.utc))
    runs.create_run(db, run)
    provider = UserProvidedCompanyProvider()
    persisted: list[Company] = []
    try:
        results = provider.search_companies(location=location, companies=[_provider_result(item) for item in request.companies], max_results=request.max_results)
        seen: set = set()
        for result in results:
            company = upsert_from_result(db, result)
            if company.id not in seen:
                runs.add_result(db, CompanyDiscoveryRunResult(discovery_run_id=run.id, company_id=company.id, provider_name=provider.name, provider_company_id=result.external_id, confidence=confidence_for(result)))
                persisted.append(company)
                seen.add(company.id)
        run.status = "completed"
        run.result_count = len(persisted)
    except Exception as exc:
        run.status = "failed"
        run.error_message = "User-provided company discovery could not be completed"
        db.commit()
        raise HTTPException(500, run.error_message) from exc
    run.completed_at = datetime.now(timezone.utc)
    db.commit()
    return runs.owned_run(db, run.id, candidate.id), [companies.by_id(db, company.id) for company in persisted]
