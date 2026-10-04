from fastapi import APIRouter

from app.api.v1.candidates import router as candidates_router
from app.api.v1.profiles import router as profiles_router
from app.api.v1.skills import router as skills_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.role_profiles import router as role_profiles_router
from app.api.v1.preferences import router as preferences_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(candidates_router)
api_router.include_router(profiles_router)
api_router.include_router(skills_router)
api_router.include_router(resumes_router)
api_router.include_router(role_profiles_router)
api_router.include_router(preferences_router)
