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
