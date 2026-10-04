from app.services.analytics_service import since
from fastapi import HTTPException
def test_period_validation():
 assert since('all') is None
 try: since('invalid')
 except HTTPException as exc: assert exc.status_code==422
 else: assert False
