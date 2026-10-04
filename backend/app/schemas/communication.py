import uuid
from typing import Literal
from pydantic import BaseModel, Field

Provider = Literal["gmail", "outlook", "mock"]

class ConnectEmail(BaseModel):
    provider: Provider
    # OAuth exchanges occur only server-side; this is an account hint, never a token.
    external_email: str | None = Field(None, max_length=255)

class AssociateCommunication(BaseModel):
    company_id: uuid.UUID | None = None
    job_id: uuid.UUID | None = None
    application_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None
    outreach_id: uuid.UUID | None = None

class ImportedEmail(BaseModel):
    external_message_id: str = Field(min_length=1, max_length=255)
    external_thread_id: str = Field(min_length=1, max_length=255)
    from_email: str | None = Field(None, max_length=255)
    from_name: str | None = Field(None, max_length=255)
    to_emails: list[str] = Field(default_factory=list)
    subject: str | None = Field(None, max_length=500)
    snippet: str | None = Field(None, max_length=1000)
    body_text: str | None = Field(None, max_length=20000)
    direction: Literal["inbound", "outbound", "unknown"] = "unknown"
    has_attachments: bool = False
