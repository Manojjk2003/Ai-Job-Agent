from app.services.job_discovery_service import title,url
def test_job_discovery_normalizes_title_and_url():assert title(' Frontend  Engineer ')=='Frontend Engineer' and url('https://x/jobs/')=='https://x/jobs'
