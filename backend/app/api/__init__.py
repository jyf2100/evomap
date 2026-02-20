"""API router configuration."""
from fastapi import APIRouter

from app.api import genes, capsules, events

api_router = APIRouter(prefix="/api/v1")

# Include all API modules
api_router.include_router(genes.router, prefix="/genes", tags=["genes"])
api_router.include_router(capsules.router, prefix="/capsules", tags=["capsules"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
