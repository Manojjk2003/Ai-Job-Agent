from sqlalchemy.orm import Session

from app.db.models.candidate import Candidate
from app.repositories.candidate_repository import create_candidate, get_candidate_by_firebase_uid


def get_or_create_candidate(db: Session, firebase_uid: str, email: str | None = None, full_name: str | None = None) -> Candidate:
    candidate = get_candidate_by_firebase_uid(db, firebase_uid)
    if candidate is not None:
        return candidate
    return create_candidate(db, firebase_uid, full_name, email)
