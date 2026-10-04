import uuid
from datetime import datetime,timezone
from sqlalchemy import DateTime,ForeignKey,Integer,String,Text,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
class ResumeVersion(Base):
 __tablename__='resume_versions';__table_args__=(UniqueConstraint('resume_id','version_number',name='uq_resume_version_number'),);id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4);resume_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('resumes.id',ondelete='CASCADE'),nullable=False,index=True);version_number:Mapped[int]=mapped_column(Integer,nullable=False);parse_status:Mapped[str]=mapped_column(String(20),nullable=False);parser_name:Mapped[str|None]=mapped_column(String(80));parser_version:Mapped[str|None]=mapped_column(String(80));extracted_text:Mapped[str|None]=mapped_column(Text);structured_sections:Mapped[dict|None]=mapped_column(JSONB);text_hash:Mapped[str|None]=mapped_column(String(64));error_message:Mapped[str|None]=mapped_column(String(500));created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc));updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc));parsed_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
