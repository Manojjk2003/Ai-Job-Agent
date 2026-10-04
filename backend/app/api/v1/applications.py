import uuid
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.application import Application,ApplicationEvent
from app.services.current_candidate_service import get_current_candidate
from app.services import application_service as service
router=APIRouter(tags=['Applications'])
class StatusChange(BaseModel):status:str=Field(pattern='^(draft|ready_for_review|approved|applied|interview|offer|rejected|withdrawn)$');note:str|None=Field(None,max_length=5000)
@router.post('/jobs/{job_id}/applications/prepare')
def prepare(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.prepare(db,get_current_candidate(db,user['uid']).id,job_id)
@router.get('/applications')
def list(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return db.query(Application).filter(Application.candidate_id==get_current_candidate(db,user['uid']).id).order_by(Application.created_at.desc()).all()
@router.get('/applications/{application_id}')
def get(application_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.owned(db,get_current_candidate(db,user['uid']).id,application_id)
@router.put('/applications/{application_id}')
def update(application_id:uuid.UUID,p:StatusChange,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.transition(db,get_current_candidate(db,user['uid']).id,application_id,p.status,p.note)
@router.post('/applications/{application_id}/mark-applied')
def applied(application_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.transition(db,get_current_candidate(db,user['uid']).id,application_id,'applied')
@router.get('/applications/{application_id}/events')
def events(application_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):service.owned(db,get_current_candidate(db,user['uid']).id,application_id);return db.query(ApplicationEvent).filter(ApplicationEvent.application_id==application_id).order_by(ApplicationEvent.created_at).all()
