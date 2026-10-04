import hashlib,uuid,zipfile
from fastapi import HTTPException,UploadFile
from sqlalchemy.exc import IntegrityError
from app.core.config import settings
from app.db.models.resume import Resume
from app.repositories import resume_repository as repo
from app.providers.storage import LocalStorageProvider
storage=LocalStorageProvider(settings.local_storage_path)
TYPES={'.pdf':'application/pdf','.docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
def _validate(filename,data):
 suffix='.'+filename.rsplit('.',1)[-1].lower() if '.' in filename else ''
 if suffix not in TYPES:raise HTTPException(422,'Only PDF and DOCX resumes are supported')
 if not data:raise HTTPException(422,'Resume file is empty')
 if len(data)>settings.max_resume_file_size_mb*1024*1024:raise HTTPException(413,'Resume file is too large')
 if suffix=='.pdf' and not data.startswith(b'%PDF'):raise HTTPException(422,'Invalid PDF file content')
 if suffix=='.docx':
  try:
   with zipfile.ZipFile(__import__('io').BytesIO(data)) as z:
    if '[Content_Types].xml' not in z.namelist():raise ValueError
  except Exception:raise HTTPException(422,'Invalid DOCX file content')
 return suffix,TYPES[suffix]
async def upload(db,candidate,file:UploadFile):
 filename=file.filename or 'resume';data=await file.read();suffix,mime=_validate(filename,data);digest=hashlib.sha256(data).hexdigest()
 if repo.duplicate(db,candidate.id,digest):raise HTTPException(409,'This resume has already been uploaded')
 rid=uuid.uuid4();key=f'candidates/{candidate.id}/resumes/{rid}{suffix}'
 storage.save(key,data)
 try:
  resume=Resume(id=rid,candidate_id=candidate.id,original_filename=filename[:255],storage_key=key,mime_type=mime,file_size=len(data),file_hash=digest,status='UPLOADED');db.add(resume);db.commit();db.refresh(resume);return resume
 except Exception:
  db.rollback();storage.delete(key);raise
def get(db,cid,id):
 resume=repo.owned(db,id,cid)
 if not resume:raise HTTPException(404,'Resume not found')
 return resume
def delete(db,cid,id):
 resume=get(db,cid,id)
 try:storage.delete(resume.storage_key)
 except Exception:raise HTTPException(500,'Unable to delete resume file')
 db.delete(resume);db.commit()
