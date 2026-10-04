import uuid
from fastapi import APIRouter,Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.services.current_candidate_service import get_current_candidate
from app.services import resume_tailoring_service as service
router=APIRouter(prefix='/jobs',tags=['Resume tailoring'])
class Reject(BaseModel):reason:str|None=Field(None,max_length=1000)
@router.post('/{job_id}/resume-tailoring')
def generate(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.generate(db,get_current_candidate(db,user['uid']).id,job_id)
@router.get('/{job_id}/resume-tailoring')
def get(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.get(db,get_current_candidate(db,user['uid']).id,job_id)
@router.post('/{job_id}/resume-tailoring/approve')
def approve(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.approve(db,get_current_candidate(db,user['uid']).id,job_id)
@router.post('/{job_id}/resume-tailoring/reject')
def reject(job_id:uuid.UUID,p:Reject,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.reject(db,get_current_candidate(db,user['uid']).id,job_id,p.reason)
@router.get('/{job_id}/resume-tailoring/download')
def download(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 return FileResponse(service.document(db,get_current_candidate(db,user['uid']).id,job_id),media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',filename='tailored-resume.docx')
