# This file is responsible for loading and validating environment variables.
# Every other file in this project imports settings from here.
# No other file should ever call os.getenv() directly.

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Pydantic reads these fields automatically from your .env file.
    If a required field is missing, the app will crash immediately at startup
    with a clear error message — which is exactly what you want.
    """
    GEMINI_API_KEY: str        # Required — no default means it must be set
    APP_ENV: str = "development"  # Optional — defaults to "development"

    class Config:
        env_file = ".env"       # Tell Pydantic where to read variables from
        env_file_encoding = "utf-8"


# Create a single shared instance.
# Every other file does: from config import settings
settings = Settings()

# This list is used by the health endpoint to check each variable.
REQUIRED_VARS = ["GEMINI_API_KEY", "APP_ENV"]