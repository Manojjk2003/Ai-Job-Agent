import uuid
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.db.models.outreach import Contact,Outreach,OutreachEvent
from app.schemas.outreach import ContactWrite,OutreachWrite
from app.services.current_candidate_service import get_current_candidate
from app.services import outreach_service as service
router=APIRouter(tags=['Outreach'])
def candidate(u,d):return get_current_candidate(d,u['uid']).id
@router.get('/companies/{company_id}/contacts')
def contacts(company_id:uuid.UUID,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return d.query(Contact).filter(Contact.company_id==company_id,Contact.candidate_id==candidate(u,d)).all()
@router.post('/companies/{company_id}/contacts')
def create_contact(company_id:uuid.UUID,p:ContactWrite,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.contact(d,candidate(u,d),company_id,p)
@router.get('/contacts/{contact_id}')
def get_contact(contact_id:uuid.UUID,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.owned_contact(d,candidate(u,d),contact_id)
@router.post('/applications/{application_id}/outreach/prepare')
def prepare(application_id:uuid.UUID,p:OutreachWrite|None=None,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.prepare(d,candidate(u,d),application_id,p)
@router.get('/outreach')
def list_outreach(u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return d.query(Outreach).filter(Outreach.candidate_id==candidate(u,d)).order_by(Outreach.created_at.desc()).all()
@router.get('/outreach/{outreach_id}')
def get_outreach(outreach_id:uuid.UUID,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):return service.owned(d,candidate(u,d),outreach_id)
@router.post('/outreach/{outreach_id}/{action}')
def change(outreach_id:uuid.UUID,action:str,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):
 mapping={'submit-review':'ready_for_review','approve':'approved','mark-sent':'sent','mark-replied':'replied','mark-cancelled':'cancelled'}
 if action not in mapping:raise HTTPException(404,'Outreach action not found')
 return service.transition(d,candidate(u,d),outreach_id,mapping[action])
@router.get('/outreach/{outreach_id}/events')
def events(outreach_id:uuid.UUID,u:dict=Depends(get_current_user),d:Session=Depends(get_db)):service.owned(d,candidate(u,d),outreach_id);return d.query(OutreachEvent).filter(OutreachEvent.outreach_id==outreach_id).order_by(OutreachEvent.created_at).all()
