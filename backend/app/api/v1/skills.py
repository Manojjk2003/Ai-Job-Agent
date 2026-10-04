from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories import skill_repository as repo
from app.schemas.skill import *
from app.services.current_candidate_service import get_current_candidate
from app.services import skill_service
router=APIRouter(tags=['Skills'])
@router.get('/skills',response_model=list[SkillResponse])
def search_skills(search:str|None=None,db:Session=Depends(get_db)):return repo.search(db,skill_service.norm(search) if search else None)
@router.get('/profile/skills',response_model=list[CandidateSkillResponse])
def list_skills(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return repo.candidate_list(db,get_current_candidate(db,user['uid']).id)
@router.post('/profile/skills',response_model=CandidateSkillResponse)
def add_skill(payload:CandidateSkillCreate,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return skill_service.add(db,get_current_candidate(db,user['uid']).id,payload.model_dump())
@router.get('/profile/skills/{candidate_skill_id}',response_model=CandidateSkillResponse)
def get_skill(candidate_skill_id,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return skill_service.get(db,get_current_candidate(db,user['uid']).id,candidate_skill_id)
@router.put('/profile/skills/{candidate_skill_id}',response_model=CandidateSkillResponse)
def put_skill(candidate_skill_id,payload:CandidateSkillUpdate,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return skill_service.update(db,get_current_candidate(db,user['uid']).id,candidate_skill_id,payload.model_dump())
@router.delete('/profile/skills/{candidate_skill_id}',status_code=204)
def del_skill(candidate_skill_id,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):skill_service.delete(db,get_current_candidate(db,user['uid']).id,candidate_skill_id)
@router.get('/profile/skills/{candidate_skill_id}/evidence',response_model=list[SkillEvidenceResponse])
def list_evidence(candidate_skill_id,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return skill_service.evidence_list(db,get_current_candidate(db,user['uid']).id,candidate_skill_id)
@router.post('/profile/skills/{candidate_skill_id}/evidence',response_model=SkillEvidenceResponse)
def add_evidence(candidate_skill_id,payload:SkillEvidenceCreate,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return skill_service.evidence_create(db,get_current_candidate(db,user['uid']).id,candidate_skill_id,payload.model_dump())
@router.put('/profile/skills/{candidate_skill_id}/evidence/{evidence_id}',response_model=SkillEvidenceResponse)
def put_evidence(candidate_skill_id,evidence_id,payload:SkillEvidenceUpdate,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return skill_service.evidence_update(db,get_current_candidate(db,user['uid']).id,candidate_skill_id,evidence_id,payload.model_dump())
@router.delete('/profile/skills/{candidate_skill_id}/evidence/{evidence_id}',status_code=204)
def del_evidence(candidate_skill_id,evidence_id,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):skill_service.evidence_delete(db,get_current_candidate(db,user['uid']).id,candidate_skill_id,evidence_id)
