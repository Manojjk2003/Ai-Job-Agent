import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
class Recommendation(Base):
 __tablename__='recommendations';id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4);candidate_id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),ForeignKey('candidates.id',ondelete='CASCADE'),nullable=False,index=True);recommendation_type:Mapped[str]=mapped_column(String(50),nullable=False);title:Mapped[str]=mapped_column(String(255),nullable=False);description:Mapped[str]=mapped_column(String(2000),nullable=False);evidence:Mapped[dict]=mapped_column(JSONB,nullable=False);priority:Mapped[str]=mapped_column(String(20),nullable=False,default='normal');confidence:Mapped[str]=mapped_column(String(30),nullable=False,default='insufficient_data');status:Mapped[str]=mapped_column(String(20),nullable=False,default='new');generation_method:Mapped[str]=mapped_column(String(30),nullable=False,default='deterministic');created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False);updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc),nullable=False)
