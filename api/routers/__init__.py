from fastapi import APIRouter

from .organization_router import router as organization_router

api_router = APIRouter()
api_router.include_router(organization_router)

__all__ = ["api_router"]
