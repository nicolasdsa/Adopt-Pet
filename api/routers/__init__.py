from fastapi import APIRouter

from .auth_router import router as auth_router
from .organization_router import router as organization_router

api_router = APIRouter()
api_router.include_router(organization_router)
api_router.include_router(auth_router)

__all__ = ["api_router"]
