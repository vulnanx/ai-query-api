# This file defines the shape of the data our /health endpoint returns.
# Pydantic uses this to validate and serialize the response automatically.

from pydantic import BaseModel
from typing import Dict

class HealthResponse(BaseModel):
    """
    This is the exact JSON structure that GET /health will return.

    Example:
    {
        "status": "ok",
        "app_env": "development",
        "checks": {
            "GEMINI_API_KEY": "set",
            "APP_ENV": "set"
        }
    }
    """
    status: str           # "ok" or "degraded"
    app_env: str          # The value of APP_ENV from your .env file
    checks: Dict[str, str]  # Maps each variable name to "set" or "missing"