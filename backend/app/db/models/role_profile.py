import uuid
from datetime import datetime,timezone
from sqlalchemy import Boolean,DateTime,ForeignKey,Integer,String,Text,UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column
from app.db.base import Base
class RoleProfile(Base):
 __tablename__='role_profiles';id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4);candidate_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False,index=True);name:Mapped[str]=mapped_column(String(255),nullable=False);target_designation:Mapped[str]=mapped_column(String(255),nullable=False);headline:Mapped[str|None]=mapped_column(String(255));summary:Mapped[str|None]=mapped_column(Text);target_seniority:Mapped[str|None]=mapped_column(String(20));is_default:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False);is_active:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc));updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))
