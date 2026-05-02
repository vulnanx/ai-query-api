# This is the entry point of the entire application.
# It creates the FastAPI app and connects all the routers.

from fastapi import FastAPI
from routes.health import router as health_router
from routes.query import router as query_router
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI application instance.
# The title and description appear in the automatic Swagger UI docs.
app = FastAPI(
    title="AI Query API",
    description="A FastAPI backend that demonstrates LLM integration with Google Gemini.",
    version="1.0.0",
)

# CORS — allows the frontend at localhost:3000 to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The frontend's URL
    allow_credentials=True,
    allow_methods=["*"],   # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],   # Allow all headers
)

# Register the health router.
# This means FastAPI now knows about the GET /health endpoint.
app.include_router(health_router)
app.include_router(query_router)

# Optional: a root endpoint so the API isn't blank at "/"
@app.get("/")
def root():
    return {"message": "AI Query API is running. Visit /docs for the interactive API explorer."}