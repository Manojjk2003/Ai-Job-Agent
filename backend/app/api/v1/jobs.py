import uuid
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.job import Job,JobSource,JobLocation
from app.schemas.job import JobWrite,JobResponse,JobDiscoveryRequest
from app.services import job_discovery_service as service
from app.services import job_normalization_service as normalization
router=APIRouter(prefix='/jobs',tags=['Jobs'])
@router.post('',response_model=JobResponse)
def add(item:JobWrite,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.add(db,item)
@router.post('/discover',response_model=list[JobResponse])
def discover(req:JobDiscoveryRequest,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return [service.add(db,x) for x in req.jobs]
@router.get('',response_model=list[JobResponse])
def list_jobs(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return db.query(Job).order_by(Job.last_seen_at.desc()).limit(100).all()
@router.get('/{job_id}',response_model=JobResponse)
def get(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 x=db.get(Job,job_id)
 if not x:raise HTTPException(404,'Job not found')
 return x
@router.get('/{job_id}/sources')
def sources(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return db.query(JobSource).filter(JobSource.job_id==job_id).all()
@router.get('/{job_id}/locations')
def locations(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return db.query(JobLocation).filter(JobLocation.job_id==job_id).all()
@router.post('/sources/{source_id}/normalize',response_model=JobResponse)
def normalize(source_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return normalization.normalize_source(db,source_id)
