from fastapi import APIRouter

from app.api.v1.candidates import router as candidates_router
from app.api.v1.profiles import router as profiles_router
from app.api.v1.skills import router as skills_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.role_profiles import router as role_profiles_router
from app.api.v1.preferences import router as preferences_router
from app.api.v1.companies import router as companies_router
from app.api.v1.hiring_sources import router as hiring_sources_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.jd_analysis import router as jd_analysis_router
from app.api.v1.matches import router as matches_router
from app.api.v1.resume_selection import router as resume_selection_router
from app.api.v1.resume_tailoring import router as resume_tailoring_router
from app.api.v1.applications import router as applications_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(candidates_router)
api_router.include_router(profiles_router)
api_router.include_router(skills_router)
api_router.include_router(resumes_router)
api_router.include_router(role_profiles_router)
api_router.include_router(preferences_router)
api_router.include_router(companies_router)
api_router.include_router(hiring_sources_router)
api_router.include_router(jobs_router)
api_router.include_router(jd_analysis_router)
api_router.include_router(matches_router)
api_router.include_router(resume_selection_router)
api_router.include_router(resume_tailoring_router)
api_router.include_router(applications_router)
