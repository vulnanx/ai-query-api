# This file defines the GET /health endpoint.
# It checks whether the app is running and whether required env vars are set.

import os
from fastapi import APIRouter
from schemas.health import HealthResponse
from config import settings, REQUIRED_VARS

# APIRouter is like a mini FastAPI app.
# We create one here, then attach it to the main app in main.py.
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Checks if the app is running and all required environment variables are set.",
)
def health_check():
    """
    For each variable in REQUIRED_VARS, we check if it exists in the environment.
    If it does, we mark it as "set". If not, "missing".
    If all variables are set, the overall status is "ok". Otherwise, "degraded".
    """

    # Build a dictionary like: {"GEMINI_API_KEY": "set", "APP_ENV": "set"}
    checks = {}
    for var in REQUIRED_VARS:
        # value = os.getenv(var)
        value = getattr(settings, var, None)
        checks[var] = "set" if value else "missing"

    # Determine overall status
    all_set = all(status == "set" for status in checks.values())
    overall_status = "ok" if all_set else "degraded"

    return HealthResponse(
        status=overall_status,
        app_env=settings.APP_ENV,
        checks=checks,
    )