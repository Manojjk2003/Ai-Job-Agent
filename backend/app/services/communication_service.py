import re, uuid
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.application import Application
from app.db.models.outreach import Contact, Outreach
from app.db.models.communication import CommunicationEvent, EmailMessage, EmailThread, Integration
from app.schemas.communication import AssociateCommunication, ConnectEmail, ImportedEmail

CLASSIFIERS = (("interview_invitation", ("interview", "schedule")), ("rejection_email", ("unfortunately", "not proceed", "rejection")), ("offer_email", ("offer",)), ("assessment_request", ("assessment", "coding test")), ("application_acknowledgement", ("thank you for applying", "application received")))
def _norm(value: str | None) -> str: return re.sub(r"^(re|fwd?):\s*", "", (value or "").strip().lower())
def classify(subject: str | None, body: str | None) -> tuple[str, str]:
    text = f"{subject or ''} {body or ''}".lower()
    for kind, signals in CLASSIFIERS:
        if any(signal in text for signal in signals): return kind, "medium"
    return "other_job_communication", "unknown"
def owned_integration(db: Session, candidate_id, integration_id):
    item = db.query(Integration).filter_by(id=integration_id, candidate_id=candidate_id).first()
    if not item: raise HTTPException(404, "Email integration not found")
    return item
def owned_message(db: Session, candidate_id, message_id):
    item = db.query(EmailMessage).filter_by(id=message_id, candidate_id=candidate_id).first()
    if not item: raise HTTPException(404, "Communication not found")
    return item
def connect(db: Session, candidate_id, payload: ConnectEmail):
    # OAuth providers need server credentials; preserve the account intent without credentials.
    item = Integration(candidate_id=candidate_id, provider=payload.provider, external_email=payload.external_email, external_account_id=payload.external_email, status="pending", scopes=["email.readonly"])
    db.add(item); db.commit(); db.refresh(item); return item
def disconnect(db: Session, candidate_id, integration_id):
    item=owned_integration(db,candidate_id,integration_id); item.status="disconnected"; item.disconnected_at=datetime.now(timezone.utc); item.credential_reference=None; db.commit(); return item
def import_message(db: Session, candidate_id, integration_id, item: ImportedEmail):
    integration=owned_integration(db,candidate_id,integration_id)
    if integration.status not in {"connected", "syncing", "pending"}: raise HTTPException(409,"Integration is not connected")
    existing=db.query(EmailMessage).filter_by(candidate_id=candidate_id,provider=integration.provider,external_message_id=item.external_message_id).first()
    if existing:return existing,False
    thread=db.query(EmailThread).filter_by(candidate_id=candidate_id,provider=integration.provider,external_thread_id=item.external_thread_id).first()
    if not thread:
        thread=EmailThread(candidate_id=candidate_id,provider=integration.provider,external_thread_id=item.external_thread_id,subject=item.subject,normalized_subject=_norm(item.subject));db.add(thread);db.flush()
    kind, confidence=classify(item.subject,item.body_text)
    msg=EmailMessage(candidate_id=candidate_id,thread_id=thread.id,integration_id=integration.id,provider=integration.provider,external_message_id=item.external_message_id,external_thread_id=item.external_thread_id,from_email=item.from_email,from_name=item.from_name,to_emails=item.to_emails,subject=item.subject,snippet=item.snippet,body_text=item.body_text,direction=item.direction,has_attachments=item.has_attachments,classification=kind,classification_confidence=confidence)
    db.add(msg);db.flush();thread.message_count+=1;thread.last_message_at=datetime.now(timezone.utc);thread.first_message_at=thread.first_message_at or thread.last_message_at
    db.add(CommunicationEvent(candidate_id=candidate_id,email_message_id=msg.id,event_type="email_received" if item.direction=="inbound" else "email_sent",metadata_json={"classification":kind}))
    integration.last_sync_at=datetime.now(timezone.utc);integration.status="connected";db.commit();db.refresh(msg);return msg,True
def associate(db: Session,candidate_id,message_id,payload:AssociateCommunication):
    msg=owned_message(db,candidate_id,message_id); thread=db.get(EmailThread,msg.thread_id)
    if payload.application_id and not db.query(Application).filter_by(id=payload.application_id,candidate_id=candidate_id).first(): raise HTTPException(404,"Application not found")
    if payload.contact_id and not db.query(Contact).filter_by(id=payload.contact_id,candidate_id=candidate_id).first(): raise HTTPException(404,"Contact not found")
    if payload.outreach_id and not db.query(Outreach).filter_by(id=payload.outreach_id,candidate_id=candidate_id).first(): raise HTTPException(404,"Outreach not found")
    for field in ("company_id","job_id","application_id","contact_id","outreach_id"): setattr(thread,field,getattr(payload,field))
    thread.association_method="manual";thread.association_confidence="high";db.commit();return msg
