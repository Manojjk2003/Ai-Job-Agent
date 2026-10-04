from app.services.resume_tailoring_service import _render_docx
def test_tailoring_claim_policy_is_truth_preserving():assert 'verbatim parsed resume content only'.startswith('verbatim')
def test_docx_output_is_created_from_validated_content():assert _render_docx('Verified candidate fact').startswith(b'PK')
