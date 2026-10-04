import json
from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.preference import CandidatePreference
from app.schemas.preference import PreferenceWrite
from app.services.current_candidate_service import get_current_candidate
router=APIRouter(prefix='/preferences',tags=['Preferences'])
def getp(d,cid):return d.scalar(select(CandidatePreference).where(CandidatePreference.candidate_id==cid))
@router.get('')
def get(u:dict=Depends(get_current_user),d:Session=Depends(get_db)):
 c=get_current_candidate(d,u['uid']);return getp(d,c.id)
@router.put('')
def put(p:PreferenceWrite,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):
 c=get_current_candidate(d,u['uid']);x=getp(d,c.id) or CandidatePreference(candidate_id=c.id)
 for k,v in p.model_dump().items():setattr(x,k,json.dumps(v) if isinstance(v,list) else v)
 d.add(x);d.commit();d.refresh(x);return x
