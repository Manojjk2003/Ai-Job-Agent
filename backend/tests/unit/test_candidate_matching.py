from app.services.candidate_matching_service import _classification,_contains
def test_matching_labels_include_partial_and_missing():assert _classification(2,2)=='strong_match' and _classification(1,2)=='partial_match' and _classification(None,2)=='missing'
def test_role_alignment_is_conservative():assert _contains('Frontend Engineer',['Frontend Engineer']) and not _contains('Backend Engineer',['Frontend Engineer'])
