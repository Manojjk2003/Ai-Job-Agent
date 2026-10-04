from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.application import Application,ApplicationEvent
from app.db.models.job import Job
from app.db.models.resume_selection import ResumeSelection
from app.db.models.tailored_resume import TailoredResume
TRANSITIONS={'draft':{'ready_for_review','withdrawn'},'ready_for_review':{'approved','withdrawn'},'approved':{'applied','withdrawn'},'applied':{'interview','offer','rejected','withdrawn'},'interview':{'offer','rejected','withdrawn'},'offer':set(),'rejected':set(),'withdrawn':set()}
def _event(db,a,typ,old=None,new=None,note=None):db.add(ApplicationEvent(application_id=a.id,event_type=typ,from_status=old,to_status=new,note=note))
def prepare(db,candidate_id,job_id):
 existing=db.query(Application).filter(Application.candidate_id==candidate_id,Application.job_id==job_id).first()
 if existing:return existing
 job=db.get(Job,job_id)
 if not job:raise HTTPException(404,'Job not found')
 selection=db.query(ResumeSelection).filter(ResumeSelection.candidate_id==candidate_id,ResumeSelection.job_id==job_id).first()
 if not selection:raise HTTPException(409,'Resume selection is required before application preparation')
 tailored=db.query(TailoredResume).filter(TailoredResume.candidate_id==candidate_id,TailoredResume.job_id==job_id,TailoredResume.status=='approved').order_by(TailoredResume.created_at.desc()).first()
 application=Application(candidate_id=candidate_id,job_id=job_id,resume_id=selection.resume_id,tailored_resume_id=tailored.id if tailored else None,application_url=job.application_url, status='ready_for_review' if job.application_url else 'draft');db.add(application);db.flush();_event(db,application,'created',None,application.status,'Prepared manually; no external submission occurred');db.commit();db.refresh(application);return application
def owned(db,candidate_id,application_id):
 value=db.query(Application).filter(Application.id==application_id,Application.candidate_id==candidate_id).first()
 if not value:raise HTTPException(404,'Application not found')
 return value
def transition(db,candidate_id,application_id,status,note=None):
 value=owned(db,candidate_id,application_id)
 if status not in TRANSITIONS.get(value.status,set()):raise HTTPException(422,'Invalid application status transition')
 if status=='applied' and not value.application_url:raise HTTPException(422,'Application URL is required before marking applied')
 old=value.status;value.status=status;_event(db,value,'status_changed',old,status,note);db.commit();db.refresh(value);return value
