from app.services.job_normalization_service import normalize_title,normalize_location
def test_deterministic_normalization():assert normalize_title(' Frontend   Engineer ')=='Frontend Engineer' and normalize_location(' Bangalore ' )=='bengaluru'
