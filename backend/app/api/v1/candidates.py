from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.candidate import CandidateResponse
from app.services.candidate_service import get_or_create_candidate

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.get("/me", response_model=CandidateResponse)
def get_my_candidate(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
) -> CandidateResponse:
    return get_or_create_candidate(
        db=db,
        firebase_uid=current_user["uid"],
        email=current_user.get("email"),
        full_name=current_user.get("name"),
    )
