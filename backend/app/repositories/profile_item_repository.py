import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session

def list_for_candidate(db: Session, model, candidate_id: uuid.UUID):
    return list(db.scalars(select(model).where(model.candidate_id == candidate_id).order_by(model.display_order, model.created_at)))
def get_owned(db: Session, model, record_id: uuid.UUID, candidate_id: uuid.UUID):
    return db.scalar(select(model).where(model.id == record_id, model.candidate_id == candidate_id))
def create(db: Session, model, candidate_id: uuid.UUID, data: dict):
    record = model(candidate_id=candidate_id, **data); db.add(record); db.commit(); db.refresh(record); return record
def update(db: Session, record, data: dict):
    for key, value in data.items(): setattr(record, key, value)
    db.commit(); db.refresh(record); return record
def delete(db: Session, record): db.delete(record); db.commit()
def get_achievement(db: Session, achievement_id: uuid.UUID, experience_id: uuid.UUID):
    from app.db.models.experience import ExperienceAchievement
    return db.scalar(select(ExperienceAchievement).where(ExperienceAchievement.id == achievement_id, ExperienceAchievement.experience_id == experience_id))
def list_achievements(db: Session, experience_id: uuid.UUID):
    from app.db.models.experience import ExperienceAchievement
    return list(db.scalars(select(ExperienceAchievement).where(ExperienceAchievement.experience_id == experience_id).order_by(ExperienceAchievement.display_order)))
def create_achievement(db: Session, experience_id: uuid.UUID, data: dict):
    from app.db.models.experience import ExperienceAchievement
    record = ExperienceAchievement(experience_id=experience_id, **data); db.add(record); db.commit(); db.refresh(record); return record
