from pathlib import Path

import firebase_admin
from firebase_admin import credentials

from app.core.config import settings


def initialize_firebase() -> bool:
    """Initialize Firebase Admin when a local service account is configured."""
    if firebase_admin._apps:
        return True
    if not settings.firebase_credentials_path:
        return False
    credential_path = Path(settings.firebase_credentials_path)
    if not credential_path.is_file():
        return False
    firebase_admin.initialize_app(credentials.Certificate(str(credential_path)))
    return True
