# Defines the POST /query endpoint.
# Right now it returns a placeholder. We will connect Gemini in Milestone 4.

from fastapi import APIRouter, HTTPException
from schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Send a Query",
    description="Send a natural language query and receive an AI-generated response.",
)
def handle_query(request: QueryRequest):
    """
    Steps this endpoint will eventually do (fully implemented by Milestone 5):
    1. Receive and validate the user's query (done — Pydantic handles this)
    2. Detect the task type (e.g., classification, extraction)
    3. Build the right system prompt
    4. Send the prompt + query to Gemini
    5. Return the response as JSON

    For now, we return a placeholder so we can test the HTTP layer.
    """

    # PLACEHOLDER — will be replaced with actual AI logic in Milestone 4
    placeholder_response = (
        f"[Placeholder] You sent: '{request.query}'. "
        "AI integration coming in Milestone 4."
    )

    return QueryResponse(message=placeholder_response)