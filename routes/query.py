# Defines the POST /query endpoint.

from fastapi import APIRouter, HTTPException
from schemas.query import QueryRequest, QueryResponse
from services.llm_service import call_llm
from prompts.task_router import build_prompt

router = APIRouter()

@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Send a Query",
    description="Send a natural language query. The system automatically detects the task type "
        "(classification, extraction, date conversion, random integer, summarization, or general) "
        "and applies the appropriate prompt before calling Google Gemini.",
)
def handle_query(request: QueryRequest):
    """
    Full request flow:
    1. Pydantic validates the request body (automatic).
    2. build_prompt() detects the task and selects the right system prompt.
    3. call_llm() sends the system prompt + user message to Gemini.
    4. The response is wrapped in QueryResponse and returned as JSON.
    """

    try:
        # Get the right system prompt for this query
        system_prompt, user_message = build_prompt(request.query)

        # Send to Gemini
        ai_response = call_llm(
            system_prompt=system_prompt,
            user_message=user_message,
        )

        # Wrap in Pydantic model before returning
        return QueryResponse(answer=ai_response)

    except Exception as e:
        # If anything goes wrong with the Gemini call, return a 500 error
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}",
        )