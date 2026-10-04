import uuid
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.job_analysis import JobAnalysis,JobRequirement
from app.services import jd_analysis_service as service
router=APIRouter(prefix='/jobs',tags=['JD analysis'])
@router.post('/{job_id}/analyze')
def analyze(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.analyze(db,job_id)
@router.get('/{job_id}/analysis')
def get(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 x=db.query(JobAnalysis).filter(JobAnalysis.job_id==job_id,JobAnalysis.status=='completed').order_by(JobAnalysis.created_at.desc()).first()
 if not x:raise HTTPException(404,'Analysis not found')
 return {'analysis':x,'requirements':db.query(JobRequirement).filter(JobRequirement.analysis_id==x.id).all()}
