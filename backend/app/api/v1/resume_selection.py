import uuid
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.resume_selection import ResumeSelection
from app.services.current_candidate_service import get_current_candidate
from app.services import resume_selection_service as service
router=APIRouter(prefix='/jobs',tags=['Resume selection'])
class Pick(BaseModel):resume_id:uuid.UUID|None=None
@router.post('/{job_id}/resume-selection')
def choose(job_id:uuid.UUID,p:Pick,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.select(db,get_current_candidate(db,user['uid']).id,job_id,p.resume_id)
@router.get('/{job_id}/resume-selection')
def get(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 x=db.query(ResumeSelection).filter(ResumeSelection.candidate_id==get_current_candidate(db,user['uid']).id,ResumeSelection.job_id==job_id).first()
 if not x:raise HTTPException(404,'Resume selection not found')
 return x
