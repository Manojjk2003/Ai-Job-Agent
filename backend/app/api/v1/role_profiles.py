from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select,update
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.role_profile import RoleProfile
from app.schemas.role_profile import RoleProfileCreate,RoleProfileWrite,RoleProfileResponse
from app.schemas.role_profile import RoleProfileLink
from app.db.models.role_profile_links import RoleProfileSkill,RoleProfileExperience,RoleProfileProject
from app.db.models.skill import CandidateSkill
from app.db.models.experience import Experience
from app.db.models.project import Project
from app.services.current_candidate_service import get_current_candidate
router=APIRouter(prefix='/role-profiles',tags=['Role Profiles'])
def c(u,d):return get_current_candidate(d,u['uid'])
def own(d,id,cid):
 x=d.scalar(select(RoleProfile).where(RoleProfile.id==id,RoleProfile.candidate_id==cid))
 if not x:raise HTTPException(404,'Role profile not found')
 return x
@router.get('',response_model=list[RoleProfileResponse])
def ls(u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return list(d.scalars(select(RoleProfile).where(RoleProfile.candidate_id==c(u,d).id)))
@router.post('',response_model=RoleProfileResponse)
def add(p:RoleProfileCreate,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):
 candidate=c(u,d)
 if p.is_default:d.execute(update(RoleProfile).where(RoleProfile.candidate_id==candidate.id).values(is_default=False))
 x=RoleProfile(candidate_id=candidate.id,**p.model_dump());d.add(x);d.commit();d.refresh(x);return x
@router.get('/{id}',response_model=RoleProfileResponse)
def get(id,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return own(d,id,c(u,d).id)
@router.put('/{id}',response_model=RoleProfileResponse)
def put(id,p:RoleProfileWrite,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):
 x=own(d,id,c(u,d).id)
 for k,v in p.model_dump().items():setattr(x,k,v)
 d.commit();d.refresh(x);return x
@router.post('/{id}/set-default',response_model=RoleProfileResponse)
def default(id,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):
 candidate=c(u,d);x=own(d,id,candidate.id);d.execute(update(RoleProfile).where(RoleProfile.candidate_id==candidate.id).values(is_default=False));x.is_default=True;d.commit();d.refresh(x);return x
@router.post('/{id}/archive',response_model=RoleProfileResponse)
def archive(id,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):x=own(d,id,c(u,d).id);x.is_active=False;x.is_default=False;d.commit();d.refresh(x);return x
def _link(model,source,field,kind):
 @router.get('/{id}/'+kind)
 def links(id,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):own(d,id,c(u,d).id);return list(d.scalars(select(model).where(model.role_profile_id==id)))
 @router.post('/{id}/'+kind)
 def add_link(id,p:RoleProfileLink,source_id,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):
  candidate=c(u,d);own(d,id,candidate.id);record=d.scalar(select(source).where(source.id==source_id,source.candidate_id==candidate.id))
  if not record:raise HTTPException(404,'Source profile record not found')
  x=model(role_profile_id=id,**{field:source_id},**p.model_dump());d.add(x);d.commit();d.refresh(x);return x
_link(RoleProfileSkill,CandidateSkill,'candidate_skill_id','skills')
_link(RoleProfileExperience,Experience,'experience_id','experiences')
_link(RoleProfileProject,Project,'project_id','projects')
