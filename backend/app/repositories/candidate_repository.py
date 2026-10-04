import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.candidate import Candidate


def get_candidate_by_id(db: Session, candidate_id: uuid.UUID) -> Candidate | None:
    return db.scalar(select(Candidate).where(Candidate.id == candidate_id))


def get_candidate_by_firebase_uid(db: Session, firebase_uid: str) -> Candidate | None:
    return db.scalar(select(Candidate).where(Candidate.firebase_uid == firebase_uid))


def create_candidate(db: Session, firebase_uid: str, full_name: str | None = None, email: str | None = None) -> Candidate:
    candidate = Candidate(firebase_uid=firebase_uid, full_name=full_name, email=email)
    db.add(candidate)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = get_candidate_by_firebase_uid(db, firebase_uid)
        if existing is not None:
            return existing
        raise
    db.refresh(candidate)
    return candidate
