from datetime import datetime,timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.company import Company
from app.db.models.job import Job
from app.db.models.application import Application
from app.db.models.outreach import Contact,Outreach,OutreachEvent
from app.providers.outreach import ManualOutreachProvider
TRANSITIONS={'draft':{'ready_for_review','cancelled'},'ready_for_review':{'approved','cancelled'},'approved':{'sent','cancelled'},'sent':{'replied','bounced'},'replied':set(),'bounced':set(),'cancelled':set()}
def norm(v):return ' '.join(v.lower().split())
def contact(db,candidate_id,company_id,payload):
 if not db.get(Company,company_id):raise HTTPException(404,'Company not found')
 value=db.query(Contact).filter(Contact.candidate_id==candidate_id,Contact.company_id==company_id,Contact.normalized_name==norm(payload.name),Contact.job_title==payload.job_title).first()
 if value:return value
 value=Contact(candidate_id=candidate_id,company_id=company_id,name=payload.name,normalized_name=norm(payload.name),job_title=payload.job_title,email=payload.email,phone=payload.phone,profile_url=payload.profile_url,source=payload.source,source_url=payload.source_url,contact_type=payload.contact_type,confidence='high' if payload.source=='user_provided' else 'unknown',is_public=payload.is_public,notes=payload.notes);db.add(value);db.commit();db.refresh(value);return value
def owned_contact(db,candidate_id,contact_id):
 value=db.query(Contact).filter(Contact.id==contact_id,Contact.candidate_id==candidate_id).first()
 if not value:raise HTTPException(404,'Contact not found')
 return value
def _event(db,o,kind,old=None,new=None):db.add(OutreachEvent(outreach_id=o.id,event_type=kind,from_status=old,to_status=new))
def prepare(db,candidate_id,application_id,payload=None):
 application=db.query(Application).filter(Application.id==application_id,Application.candidate_id==candidate_id).first()
 if not application:raise HTTPException(404,'Application not found')
 job=db.get(Job,application.job_id);company=db.get(Company,job.company_id)
 contact_value=owned_contact(db,candidate_id,payload.contact_id) if payload and payload.contact_id else None
 if contact_value and contact_value.company_id!=company.id:raise HTTPException(422,'Contact does not belong to application company')
 existing=db.query(Outreach).filter(Outreach.candidate_id==candidate_id,Outreach.application_id==application_id,Outreach.contact_id==getattr(contact_value,'id',None)).first()
 if existing:return existing
 data=payload or ManualOutreachProvider().prepare({'job_title':job.canonical_title,'company_name':company.canonical_name})
 subject=data.subject if payload else data['subject'];body=data.body if payload else data['body'];value=Outreach(candidate_id=candidate_id,company_id=company.id,job_id=job.id,application_id=application.id,contact_id=getattr(contact_value,'id',None),channel=payload.channel if payload else 'email',subject=subject,body=body,call_to_action=getattr(payload,'call_to_action',None),draft_method='manual' if payload else 'template');db.add(value);db.flush();_event(db,value,'draft_created',None,'draft');db.commit();db.refresh(value);return value
def owned(db,candidate_id,outreach_id):
 value=db.query(Outreach).filter(Outreach.id==outreach_id,Outreach.candidate_id==candidate_id).first()
 if not value:raise HTTPException(404,'Outreach not found')
 return value
def transition(db,candidate_id,outreach_id,target):
 value=owned(db,candidate_id,outreach_id)
 if target not in TRANSITIONS.get(value.status,set()):raise HTTPException(422,'Invalid outreach lifecycle transition')
 old=value.status;value.status=target
 if target=='approved':value.approved_at=datetime.now(timezone.utc)
 if target=='sent':value.sent_at=datetime.now(timezone.utc)
 _event(db,value,'status_changed',old,target);db.commit();db.refresh(value);return value
