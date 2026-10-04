import pytest
from app.schemas.hiring_source import HiringSourceWrite
from app.services.hiring_source_discovery_service import normalize_url
def test_normalize_hiring_source_url():assert normalize_url('https://www.Example.com/careers/')=='https://example.com/careers'
def test_rejects_unsafe_source_url():
 with pytest.raises(ValueError):HiringSourceWrite(name='x',source_type='official_careers',source_url='javascript:x')
