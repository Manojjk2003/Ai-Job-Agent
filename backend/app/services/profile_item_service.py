import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import profile_item_repository as repo

def list_items(db: Session, model, candidate_id: uuid.UUID): return repo.list_for_candidate(db, model, candidate_id)
def get_item(db: Session, model, record_id: uuid.UUID, candidate_id: uuid.UUID):
    record = repo.get_owned(db, model, record_id, candidate_id)
    if record is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile record not found")
    return record
def create_item(db: Session, model, candidate_id: uuid.UUID, data: dict): return repo.create(db, model, candidate_id, data)
def update_item(db: Session, model, record_id: uuid.UUID, candidate_id: uuid.UUID, data: dict): return repo.update(db, get_item(db, model, record_id, candidate_id), data)
def delete_item(db: Session, model, record_id: uuid.UUID, candidate_id: uuid.UUID): repo.delete(db, get_item(db, model, record_id, candidate_id))
def get_experience_achievement(db: Session, experience_id: uuid.UUID, achievement_id: uuid.UUID, candidate_id: uuid.UUID):
    from app.db.models.experience import Experience
    get_item(db, Experience, experience_id, candidate_id)
    result = repo.get_achievement(db, achievement_id, experience_id)
    if result is None: raise HTTPException(status_code=404, detail="Achievement not found")
    return result
