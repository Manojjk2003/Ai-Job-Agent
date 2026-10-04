import uuid

from pydantic import BaseModel, ConfigDict


class CandidateResponse(BaseModel):
    id: uuid.UUID
    firebase_uid: str
    email: str | None
    full_name: str | None

    model_config = ConfigDict(from_attributes=True)
