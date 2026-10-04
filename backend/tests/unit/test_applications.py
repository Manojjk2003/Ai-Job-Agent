from app.services.application_service import TRANSITIONS
def test_application_transition_rules_are_controlled():assert 'applied' in TRANSITIONS['approved'] and 'applied' not in TRANSITIONS['draft']
