import uuid
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.candidate_job_match import CandidateJobMatch,CandidateJobMatchEvidence
from app.services.current_candidate_service import get_current_candidate
from app.services import candidate_matching_service as service
router=APIRouter(prefix='/jobs',tags=['Candidate matching'])
@router.post('/{job_id}/match')
def match(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.match(db,get_current_candidate(db,user['uid']).id,job_id)
@router.get('/{job_id}/match')
def get(job_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 x=db.query(CandidateJobMatch).filter(CandidateJobMatch.candidate_id==get_current_candidate(db,user['uid']).id,CandidateJobMatch.job_id==job_id).first()
 if not x:raise HTTPException(404,'Match not found')
 return {'match':x,'evidence':db.query(CandidateJobMatchEvidence).filter(CandidateJobMatchEvidence.match_id==x.id).all()}
