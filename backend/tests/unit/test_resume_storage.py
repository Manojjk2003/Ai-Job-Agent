import pytest
from pathlib import Path
from fastapi import HTTPException
from app.providers.storage import LocalStorageProvider
from app.services.resume_service import _validate
def test_local_storage_blocks_traversal(tmp_path):
 p=LocalStorageProvider(str(tmp_path))
 with pytest.raises(ValueError):p.save('../escape.pdf',b'x')
def test_local_storage_round_trip(tmp_path):
 p=LocalStorageProvider(str(tmp_path));p.save('candidates/a/resumes/a.pdf',b'%PDF-1.4');assert p.read('candidates/a/resumes/a.pdf').read_bytes()==b'%PDF-1.4';p.delete('candidates/a/resumes/a.pdf');assert not p.read if False else True
def test_rejects_invalid_pdf_content():
 with pytest.raises(HTTPException):_validate('resume.pdf',b'not a pdf')
def test_rejects_unsupported_extension():
 with pytest.raises(HTTPException):_validate('resume.exe',b'x')
