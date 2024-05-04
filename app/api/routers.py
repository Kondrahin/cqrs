"""Configuration of routers for all endpoints."""
from fastapi import APIRouter

from app.api.endpoints.commands import router_commands
from app.api.endpoints.query import router_query

router = APIRouter()

router.include_router(router_commands)
router.include_router(router_query)
