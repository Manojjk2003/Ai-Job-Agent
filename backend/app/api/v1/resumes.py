from fastapi import APIRouter,Depends,UploadFile,File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories import resume_repository as repo
from app.schemas.resume import ResumeResponse
from app.services.current_candidate_service import get_current_candidate
from app.services import resume_service
router=APIRouter(prefix='/resumes',tags=['Resumes'])
def c(user,db):return get_current_candidate(db,user['uid'])
@router.post('',response_model=ResumeResponse)
async def upload(file:UploadFile=File(...),user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return await resume_service.upload(db,c(user,db),file)
@router.get('',response_model=list[ResumeResponse])
def list_resumes(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return repo.list_for_candidate(db,c(user,db).id)
@router.get('/{resume_id}',response_model=ResumeResponse)
def get_resume(resume_id,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return resume_service.get(db,c(user,db).id,resume_id)
@router.get('/{resume_id}/download')
def download(resume_id,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 r=resume_service.get(db,c(user,db).id,resume_id)
 try:path=resume_service.storage.read(r.storage_key)
 except FileNotFoundError:raise __import__('fastapi').HTTPException(500,'Resume file is unavailable')
 return FileResponse(path,media_type=r.mime_type,filename=r.original_filename)
@router.delete('/{resume_id}',status_code=204)
def delete_resume(resume_id,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):resume_service.delete(db,c(user,db).id,resume_id)
