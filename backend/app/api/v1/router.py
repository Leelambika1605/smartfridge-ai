from fastapi import APIRouter
from app.api.v1.endpoints import health, auth

api_router = APIRouter()

# Mount health routes
api_router.include_router(health.router, prefix="", tags=["Health"])

# Mount authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["User Authentication & Multi-Tenancy"])
