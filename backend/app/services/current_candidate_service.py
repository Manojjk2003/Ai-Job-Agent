from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.candidate import Candidate
from app.repositories.candidate_repository import get_candidate_by_firebase_uid


def get_current_candidate(db: Session, firebase_uid: str) -> Candidate:
    candidate = get_candidate_by_firebase_uid(db, firebase_uid)
    if candidate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate profile not found")
    return candidate
