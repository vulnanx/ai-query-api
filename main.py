# This is the entry point of the entire application.
# It creates the FastAPI app and connects all the routers.

from fastapi import FastAPI
from routes.health import router as health_router
from routes.query import router as query_router

# Create the FastAPI application instance.
# The title and description appear in the automatic Swagger UI docs.
app = FastAPI(
    title="AI Query API",
    description="A FastAPI backend that demonstrates LLM integration with Google Gemini.",
    version="1.0.0",
)

# Register the health router.
# This means FastAPI now knows about the GET /health endpoint.
app.include_router(health_router)
app.include_router(query_router)

# Optional: a root endpoint so the API isn't blank at "/"
@app.get("/")
def root():
    return {"message": "AI Query API is running. Visit /docs for the interactive API explorer."}