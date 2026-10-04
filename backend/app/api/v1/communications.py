import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.models.communication import EmailMessage, EmailThread, Integration
from app.db.session import get_db
from app.schemas.communication import AssociateCommunication, ConnectEmail, ImportedEmail
from app.services.current_candidate_service import get_current_candidate
from app.services import communication_service as service
router=APIRouter(tags=["Communications"])
def cid(user,db): return get_current_candidate(db,user["uid"]).id
@router.get("/integrations")
def integrations(user:dict=Depends(get_current_user),db:Session=Depends(get_db)): return db.query(Integration).filter_by(candidate_id=cid(user,db)).all()
@router.post("/integrations/email/connect")
def connect(payload:ConnectEmail,user:dict=Depends(get_current_user),db:Session=Depends(get_db)): return service.connect(db,cid(user,db),payload)
@router.post("/integrations/email/{integration_id}/disconnect")
def disconnect(integration_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)): return service.disconnect(db,cid(user,db),integration_id)
@router.get("/integrations/email/{integration_id}/sync-status")
def sync_status(integration_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)): return service.owned_integration(db,cid(user,db),integration_id)
# Internal deterministic import endpoint for an already-authorized provider adapter; not an OAuth token endpoint.
@router.post("/integrations/email/{integration_id}/sync/import")
def import_one(integration_id:uuid.UUID,payload:ImportedEmail,user:dict=Depends(get_current_user),db:Session=Depends(get_db)): return {"message":service.import_message(db,cid(user,db),integration_id,payload)[0]}
@router.get("/communications")
def communications(application_id:uuid.UUID|None=None,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 q=db.query(EmailMessage).filter_by(candidate_id=cid(user,db))
 if application_id:
  thread_ids=[x[0] for x in db.query(EmailThread.id).filter_by(candidate_id=cid(user,db),application_id=application_id).all()];q=q.filter(EmailMessage.thread_id.in_(thread_ids))
 return q.order_by(EmailMessage.received_at.desc()).all()
@router.get("/communications/{message_id}")
def communication(message_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)): return service.owned_message(db,cid(user,db),message_id)
@router.post("/communications/{message_id}/associate")
def associate(message_id:uuid.UUID,payload:AssociateCommunication,user:dict=Depends(get_current_user),db:Session=Depends(get_db)): return service.associate(db,cid(user,db),message_id,payload)
@router.get("/applications/{application_id}/communications")
def application_communications(application_id:uuid.UUID,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
 if not db.query(__import__('app.db.models.application',fromlist=['Application']).Application).filter_by(id=application_id,candidate_id=cid(user,db)).first():raise HTTPException(404,"Application not found")
 return communications(application_id,user,db)
