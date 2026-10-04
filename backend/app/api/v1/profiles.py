from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.candidate_profile import CandidateProfileCreate, CandidateProfileResponse
from app.services.candidate_profile_service import create_candidate_profile, get_candidate_profile
from app.services.current_candidate_service import get_current_candidate

router = APIRouter(prefix="/profile", tags=["Candidate Profile"])


@router.get("", response_model=CandidateProfileResponse | None)
def get_my_profile(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
) -> CandidateProfileResponse | None:
    candidate = get_current_candidate(db, current_user["uid"])
    return get_candidate_profile(db, candidate.id)


@router.post("", response_model=CandidateProfileResponse)
def create_my_profile(
    payload: CandidateProfileCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CandidateProfileResponse:
    candidate = get_current_candidate(db, current_user["uid"])
    return create_candidate_profile(db, candidate.id, payload.model_dump(mode="json"))
