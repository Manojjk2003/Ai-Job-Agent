import uuid

from sqlalchemy.orm import Session

from app.db.models.candidate_profile import CandidateProfile
from app.repositories.candidate_profile_repository import create_profile, get_profile_by_candidate_id, update_profile


def get_candidate_profile(db: Session, candidate_id: uuid.UUID) -> CandidateProfile | None:
    return get_profile_by_candidate_id(db, candidate_id)


def create_candidate_profile(db: Session, candidate_id: uuid.UUID, data: dict) -> CandidateProfile:
    existing = get_profile_by_candidate_id(db, candidate_id)
    return existing if existing is not None else create_profile(db, candidate_id, data)


def update_candidate_profile(db: Session, candidate_id: uuid.UUID, data: dict) -> CandidateProfile:
    profile = get_profile_by_candidate_id(db, candidate_id)
    return create_profile(db, candidate_id, data) if profile is None else update_profile(db, profile, data)

def profile_completeness(db: Session, candidate_id: uuid.UUID) -> dict[str, int | bool]:
    from app.db.models.education import Education
    from app.db.models.experience import Experience
    from app.db.models.project import Project
    sections = [get_candidate_profile(db, candidate_id) is not None, bool(db.query(Experience).filter_by(candidate_id=candidate_id).first()), bool(db.query(Education).filter_by(candidate_id=candidate_id).first()), bool(db.query(Project).filter_by(candidate_id=candidate_id).first())]
    return {"completed_sections": sum(sections), "total_sections": len(sections), "percentage": round(sum(sections) * 100 / len(sections))}
