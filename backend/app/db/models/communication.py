import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def now() -> datetime:
    return datetime.now(timezone.utc)


class Integration(Base):
    __tablename__ = "integrations"
    __table_args__ = (UniqueConstraint("candidate_id", "provider", "external_account_id", name="uq_candidate_email_integration"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(30), nullable=False)
    integration_type: Mapped[str] = mapped_column(String(30), nullable=False, default="email")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    external_account_id: Mapped[str | None] = mapped_column(String(255))
    external_email: Mapped[str | None] = mapped_column(String(255))
    scopes: Mapped[list | None] = mapped_column(JSONB)
    # A server-side reference only; never an OAuth token.
    credential_reference: Mapped[str | None] = mapped_column(String(255))
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sync_cursor: Mapped[str | None] = mapped_column(String(1024))
    last_error: Mapped[str | None] = mapped_column(String(1000))
    connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    disconnected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)


class EmailThread(Base):
    __tablename__ = "email_threads"
    __table_args__ = (UniqueConstraint("candidate_id", "provider", "external_thread_id", name="uq_candidate_provider_thread"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(30), nullable=False)
    external_thread_id: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(500))
    normalized_subject: Mapped[str | None] = mapped_column(String(500), index=True)
    first_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_message_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    message_count: Mapped[int] = mapped_column(default=0, nullable=False)
    company_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="SET NULL"))
    job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="SET NULL"))
    application_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="SET NULL"))
    contact_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("contacts.id", ondelete="SET NULL"))
    outreach_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("outreach.id", ondelete="SET NULL"))
    association_method: Mapped[str] = mapped_column(String(30), nullable=False, default="unknown")
    association_confidence: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)


class EmailMessage(Base):
    __tablename__ = "email_messages"
    __table_args__ = (UniqueConstraint("candidate_id", "provider", "external_message_id", name="uq_candidate_provider_message"),)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    thread_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("email_threads.id", ondelete="CASCADE"), nullable=False, index=True)
    integration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(30), nullable=False)
    external_message_id: Mapped[str] = mapped_column(String(255), nullable=False)
    external_thread_id: Mapped[str] = mapped_column(String(255), nullable=False)
    from_email: Mapped[str | None] = mapped_column(String(255))
    from_name: Mapped[str | None] = mapped_column(String(255))
    to_emails: Mapped[list | None] = mapped_column(JSONB)
    subject: Mapped[str | None] = mapped_column(String(500))
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    direction: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    snippet: Mapped[str | None] = mapped_column(String(1000))
    body_text: Mapped[str | None] = mapped_column(Text)
    has_attachments: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    classification: Mapped[str] = mapped_column(String(50), nullable=False, default="other_job_communication")
    classification_confidence: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)


class CommunicationEvent(Base):
    __tablename__ = "communication_events"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    email_message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("email_messages.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, nullable=False)
