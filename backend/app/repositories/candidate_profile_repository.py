import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.candidate_profile import CandidateProfile


def get_profile_by_candidate_id(db: Session, candidate_id: uuid.UUID) -> CandidateProfile | None:
    return db.scalar(select(CandidateProfile).where(CandidateProfile.candidate_id == candidate_id))


def create_profile(db: Session, candidate_id: uuid.UUID, data: dict) -> CandidateProfile:
    profile = CandidateProfile(candidate_id=candidate_id, **data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, profile: CandidateProfile, data: dict) -> CandidateProfile:
    for field, value in data.items():
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile
