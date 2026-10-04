import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class Resume(Base):
 __tablename__='resumes';__table_args__=(UniqueConstraint('candidate_id','file_hash',name='uq_candidate_resume_hash'),);id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4);candidate_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False,index=True);original_filename:Mapped[str]=mapped_column(String(255),nullable=False);storage_key:Mapped[str]=mapped_column(String(500),unique=True,nullable=False);mime_type:Mapped[str]=mapped_column(String(100),nullable=False);file_size:Mapped[int]=mapped_column(Integer,nullable=False);file_hash:Mapped[str]=mapped_column(String(64),nullable=False);status:Mapped[str]=mapped_column(String(20),nullable=False,default='UPLOADED');created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc));updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))
