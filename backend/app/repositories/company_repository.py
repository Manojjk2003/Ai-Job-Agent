from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.db.models.company import Company, CompanyLocation


def by_id(db: Session, company_id):
    return db.scalar(select(Company).options(selectinload(Company.locations)).where(Company.id == company_id))


def by_domain(db: Session, domain: str | None):
    return db.scalar(select(Company).options(selectinload(Company.locations)).where(Company.website_domain == domain)) if domain else None


def by_normalized_name(db: Session, name: str):
    return db.scalar(select(Company).options(selectinload(Company.locations)).where(Company.normalized_name == name))


def search(db: Session, *, query: str | None, city: str | None, area: str | None, status: str | None, limit: int, offset: int):
    statement = select(Company).options(selectinload(Company.locations)).order_by(Company.canonical_name).offset(offset).limit(limit)
    if query:
        pattern = f"%{query.strip()}%"
        statement = statement.where(or_(Company.canonical_name.ilike(pattern), Company.website_domain.ilike(pattern)))
    if status:
        statement = statement.where(Company.status == status)
    if city or area:
        statement = statement.join(CompanyLocation)
        if city:
            statement = statement.where(CompanyLocation.city.ilike(city.strip()))
        if area:
            statement = statement.where(CompanyLocation.area.ilike(area.strip()))
    return list(db.scalars(statement).unique())


def location_by_normalized_name(db: Session, company_id, normalized_location: str):
    return db.scalar(select(CompanyLocation).where(CompanyLocation.company_id == company_id, CompanyLocation.normalized_location == normalized_location))
