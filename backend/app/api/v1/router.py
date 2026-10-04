from fastapi import APIRouter

from app.api.v1.candidates import router as candidates_router
from app.api.v1.profiles import router as profiles_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(candidates_router)
api_router.include_router(profiles_router)
