import uuid
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.repositories import hiring_source_repository as repo
from app.schemas.hiring_source import CompanyHiringSourceResponse,HiringSourceDiscoveryRequest,HiringSourceDiscoveryResponse,HiringSourceWrite
from app.services import hiring_source_discovery_service as service
router=APIRouter(tags=['Hiring sources'])
@router.get('/companies/{company_id}/hiring-sources',response_model=list[CompanyHiringSourceResponse])
def list_sources(company_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):service.company(db,company_id);return repo.list_for_company(db,company_id)
@router.post('/companies/{company_id}/hiring-sources',response_model=CompanyHiringSourceResponse)
def add(company_id:uuid.UUID,item:HiringSourceWrite,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return service.add(db,company_id,item)
@router.post('/companies/{company_id}/hiring-sources/discover',response_model=HiringSourceDiscoveryResponse)
def discover(company_id:uuid.UUID,request:HiringSourceDiscoveryRequest,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):return {'company_id':company_id,'status':'completed','sources':service.discover(db,company_id,request.sources)}
@router.get('/hiring-sources/{hiring_source_id}')
def get_source(hiring_source_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 from app.db.models.hiring_source import HiringSource
 value=db.get(HiringSource,hiring_source_id)
 if not value:raise HTTPException(404,'Hiring source not found')
 return value
