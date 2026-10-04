from app.services.outreach_service import TRANSITIONS,norm
def test_outreach_lifecycle_requires_approval_before_manual_sent():assert 'sent' not in TRANSITIONS['draft'] and 'sent' in TRANSITIONS['approved']
def test_contact_normalization_is_conservative():assert norm(' Jane  Doe ')=='jane doe'
