from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.services.current_candidate_service import get_current_candidate
from app.services import analytics_service as service
router=APIRouter(prefix='/analytics',tags=['Analytics'])
def c(u,d):return get_current_candidate(d,u['uid']).id
@router.get('/overview')
def overview(period:str='30d',u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.overview(d,c(u,d),period)
@router.get('/funnel')
def funnel(period:str='30d',u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.funnel(d,c(u,d),period)
@router.get('/outreach')
def outreach(period:str='30d',u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.outreach(d,c(u,d),period)
@router.get('/matches')
def matches(period:str='30d',u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.matches(d,c(u,d),period)
@router.get('/skills')
def skills(period:str='30d',u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.skills(d,c(u,d),period)
@router.get('/recommendations')
def recommendations(u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.recommendations(d,c(u,d))
