from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.company import CompanyDiscoveryRun, CompanyDiscoveryRunResult


def create_run(db: Session, run: CompanyDiscoveryRun) -> CompanyDiscoveryRun:
    db.add(run)
    db.flush()
    return run


def add_result(db: Session, result: CompanyDiscoveryRunResult) -> None:
    db.add(result)


def list_for_candidate(db: Session, candidate_id, limit: int = 50):
    return list(db.scalars(select(CompanyDiscoveryRun).where(CompanyDiscoveryRun.candidate_id == candidate_id).order_by(CompanyDiscoveryRun.created_at.desc()).limit(limit)))


def owned_run(db: Session, run_id, candidate_id):
    return db.scalar(select(CompanyDiscoveryRun).where(CompanyDiscoveryRun.id == run_id, CompanyDiscoveryRun.candidate_id == candidate_id))
