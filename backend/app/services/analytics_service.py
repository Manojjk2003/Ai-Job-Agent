from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models.application import Application
from app.db.models.candidate_job_match import CandidateJobMatch
from app.db.models.communication import CommunicationEvent, EmailMessage
from app.db.models.job_analysis import JobSkill
from app.db.models.outreach import Outreach
from app.db.models.skill import CandidateSkill, Skill
from app.db.models.analytics import Recommendation

def since(period:str):
 values={'7d':7,'30d':30,'90d':90,'6m':180,'1y':365,'all':None}
 if period not in values: raise HTTPException(422,'Unsupported analytics period')
 return None if values[period] is None else datetime.now(timezone.utc)-timedelta(days=values[period])
def _query(q, field, point): return q if point is None else q.filter(field>=point)
def overview(db:Session,candidate_id,period='30d'):
 point=since(period); apps=_query(db.query(Application).filter_by(candidate_id=candidate_id),Application.created_at,point).all(); total=len(apps); eligible=[a for a in apps if a.status not in {'draft','ready_for_review'} and (not point or a.created_at<=datetime.now(timezone.utc)-timedelta(days=14))]; ids=[a.id for a in apps]
 threads=[]
 from app.db.models.communication import EmailThread
 if ids: threads=[x[0] for x in db.query(EmailThread.application_id).filter(EmailThread.candidate_id==candidate_id,EmailThread.application_id.in_(ids)).all()]
 responses=0 if not threads else db.query(EmailMessage).filter(EmailMessage.candidate_id==candidate_id,EmailMessage.thread_id.in_(threads),EmailMessage.direction=='inbound').count()
 statuses=[a.status for a in apps]
 return {'period':period,'applications':{'total':total,'active':sum(s in {'applied','interview','offer'} for s in statuses),'rejected':statuses.count('rejected'),'interviewing':statuses.count('interview'),'offers':statuses.count('offer')},'responses':{'count':responses,'rate':round(responses/len(eligible),4) if eligible else None,'eligible_applications':len(eligible)},'interviews':{'count':statuses.count('interview'),'rate':round(statuses.count('interview')/len(eligible),4) if eligible else None},'offers':{'count':statuses.count('offer')}}
def funnel(db,candidate_id,period='30d'):
 point=since(period); apps=_query(db.query(Application).filter_by(candidate_id=candidate_id),Application.created_at,point).all(); jobs=[a.job_id for a in apps]; matches=0 if not jobs else _query(db.query(CandidateJobMatch).filter(CandidateJobMatch.candidate_id==candidate_id,CandidateJobMatch.job_id.in_(jobs)),CandidateJobMatch.created_at,point).count();o=overview(db,candidate_id,period)
 return {'period':period,'matched':matches,'prepared':sum(a.status in {'ready_for_review','approved','applied','interview','offer','rejected','withdrawn'} for a in apps),'applied':sum(a.status in {'applied','interview','offer','rejected','withdrawn'} for a in apps),'responses':o['responses']['count'],'interviews':o['interviews']['count'],'offers':o['offers']['count']}
def outreach(db,candidate_id,period='30d'):
 point=since(period); rows=_query(db.query(Outreach).filter_by(candidate_id=candidate_id),Outreach.created_at,point).all();sent=sum(x.status in {'sent','replied'} for x in rows);replied=sum(x.status=='replied' for x in rows);return {'period':period,'sent':sent,'replied':replied,'bounced':sum(x.status=='bounced' for x in rows),'cancelled':sum(x.status=='cancelled' for x in rows),'response_rate':round(replied/sent,4) if sent else None,'sample_size':sent}
def matches(db,candidate_id,period='30d'):
 point=since(period); rows=_query(db.query(CandidateJobMatch).filter_by(candidate_id=candidate_id),CandidateJobMatch.created_at,point).all();return {'period':period,'strong_match':sum(x.status=='strong_match' for x in rows),'partial_match':sum(x.status=='partial_match' for x in rows),'missing':sum(x.status=='missing' for x in rows),'unknown':sum(x.status=='unknown' for x in rows)}
def skills(db,candidate_id,period='30d'):
 point=since(period); q=db.query(Skill.name,func.count(JobSkill.id)).join(JobSkill,JobSkill.skill_id==Skill.id)
 # Job skills are global canonical demand; candidate coverage is individually resolved.
 rows=q.group_by(Skill.name).order_by(func.count(JobSkill.id).desc()).limit(20).all();own={x[0] for x in db.query(CandidateSkill.skill_id).filter_by(candidate_id=candidate_id).all()};ids={x[0]:x[1] for x in db.query(Skill.id,Skill.name).all()};return {'period':period,'skills':[{'skill':name,'job_count':count,'candidate_has':ids.get(name) in own} for name,count in rows]}
def recommendations(db,candidate_id):
 o=overview(db,candidate_id);rows=[]
 if o['applications']['total']<5: rows.append({'recommendation_type':'application_strategy','title':'Build more tracked application evidence','description':'You have fewer than five tracked applications, so outcome patterns are still early.','evidence':{'applications':o['applications']['total']},'confidence':'insufficient_data'})
 else: rows.append({'recommendation_type':'search_strategy','title':'Continue tracking application outcomes','description':'Use your tracked responses and interviews to compare strategies as sample sizes grow.','evidence':{'applications':o['applications']['total'],'responses':o['responses']['count']},'confidence':'early_signal'})
 return rows
