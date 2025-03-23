from fastapi import APIRouter
from .auth import auth_router
from .profile import profile_router



api_version_one = APIRouter(prefix="/api/v1")


api_version_one.include_router(auth_router)
api_version_one.include_router(profile_router)