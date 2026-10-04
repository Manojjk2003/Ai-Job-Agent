from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.candidate_profile import CandidateProfileCreate, CandidateProfileResponse, CandidateProfileUpdate
from app.schemas.profile_items import *
from app.services.candidate_profile_service import create_candidate_profile, get_candidate_profile, update_candidate_profile, profile_completeness
from app.services.current_candidate_service import get_current_candidate
from app.db.models.experience import Experience
from app.db.models.education import Education
from app.db.models.project import Project
from app.repositories import profile_item_repository as item_repo
from app.services import profile_item_service as items

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

@router.put("", response_model=CandidateProfileResponse)
def update_my_profile(payload: CandidateProfileUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    candidate = get_current_candidate(db, current_user["uid"])
    return update_candidate_profile(db, candidate.id, payload.model_dump(mode="json"))

@router.get("/completeness")
def get_completeness(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return profile_completeness(db, get_current_candidate(db, current_user["uid"]).id)

def _candidate(user, db): return get_current_candidate(db, user["uid"])
def _crud(model, create_schema, update_schema, response_schema, plural):
    @router.get(f"/{plural}", response_model=list[response_schema])
    def list_records(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        return items.list_items(db, model, _candidate(current_user, db).id)
    @router.post(f"/{plural}", response_model=response_schema)
    def create_record(payload: create_schema, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        return items.create_item(db, model, _candidate(current_user, db).id, payload.model_dump(mode="json"))
    @router.get(f"/{plural}/{{record_id}}", response_model=response_schema)
    def get_record(record_id, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        return items.get_item(db, model, record_id, _candidate(current_user, db).id)
    @router.put(f"/{plural}/{{record_id}}", response_model=response_schema)
    def update_record(record_id, payload: update_schema, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        return items.update_item(db, model, record_id, _candidate(current_user, db).id, payload.model_dump(mode="json"))
    @router.delete(f"/{plural}/{{record_id}}", status_code=204)
    def delete_record(record_id, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        items.delete_item(db, model, record_id, _candidate(current_user, db).id)

_crud(Experience, ExperienceCreate, ExperienceUpdate, ExperienceResponse, "experiences")
_crud(Education, EducationCreate, EducationUpdate, EducationResponse, "education")
_crud(Project, ProjectCreate, ProjectUpdate, ProjectResponse, "projects")

@router.post("/experiences/{experience_id}/achievements", response_model=ExperienceAchievementResponse)
def create_achievement(experience_id, payload: ExperienceAchievementCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    candidate = _candidate(current_user, db); items.get_item(db, Experience, experience_id, candidate.id)
    return item_repo.create_achievement(db, experience_id, payload.model_dump())
@router.put("/experiences/{experience_id}/achievements/{achievement_id}", response_model=ExperienceAchievementResponse)
def update_achievement(experience_id, achievement_id, payload: ExperienceAchievementUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    achievement = items.get_experience_achievement(db, experience_id, achievement_id, _candidate(current_user, db).id)
    return item_repo.update(db, achievement, payload.model_dump())
@router.delete("/experiences/{experience_id}/achievements/{achievement_id}", status_code=204)
def delete_achievement(experience_id, achievement_id, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    item_repo.delete(db, items.get_experience_achievement(db, experience_id, achievement_id, _candidate(current_user, db).id))
