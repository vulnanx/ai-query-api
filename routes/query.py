# Defines the POST /query endpoint.
# Right now it returns a placeholder. We will connect Gemini in Milestone 4.

from fastapi import APIRouter, HTTPException
from schemas.query import QueryRequest, QueryResponse
from services.llm_service import call_llm

router = APIRouter()

DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant integrated into a FastAPI backend application.
Answer the user's questions clearly, concisely, and accurately.
If the user asks you to perform a specific task like classification,
information extraction, or date conversion, do it precisely.
"""

@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Send a Query",
    description="Send a natural language query and receive an AI-generated response.",
)
def handle_query(request: QueryRequest):
    """
    Receives the user's query, sends it to Gemini, and returns the response.
    """

    try:
        # Call Gemini with the default system prompt and the user's query
        ai_response = call_llm(
            system_prompt=DEFAULT_SYSTEM_PROMPT,
            user_message=request.query,
        )

        return QueryResponse(message=ai_response)

    except Exception as e:
        # If anything goes wrong with the Gemini call, return a 500 error
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}",
        )