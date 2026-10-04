from abc import ABC, abstractmethod
from dataclasses import dataclass

class EmailProviderError(RuntimeError): pass

@dataclass(frozen=True)
class NormalizedEmailMessage:
    external_message_id: str
    external_thread_id: str
    from_email: str | None
    from_name: str | None
    to_emails: list[str]
    subject: str | None
    snippet: str | None
    body_text: str | None
    direction: str = "unknown"
    has_attachments: bool = False

class EmailProvider(ABC):
    """Read-only sync contract. Sending is deliberately a separate future capability."""
    name: str
    @abstractmethod
    def authorization_url(self, state: str) -> str: ...
    @abstractmethod
    def sync_messages(self, *, cursor: str | None) -> tuple[list[NormalizedEmailMessage], str | None]: ...
