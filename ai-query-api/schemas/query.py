# Defines the shape of the request body and response body for POST /query.

from pydantic import BaseModel, field_validator

class QueryRequest(BaseModel):
    """
    This is what the user must send in the request body.

    Example request body:
    {
        "query": "What is machine learning?"
    }
    """
    query: str  # Must be a non-empty string

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, value: str) -> str:
        """
        This validator runs automatically when a request comes in.
        If the query is empty or just whitespace, we reject it with a clear error.
        """
        if not value.strip():
            raise ValueError("Query cannot be empty or whitespace.")
        return value.strip()  # Remove leading/trailing spaces


class QueryResponse(BaseModel):
    """
    This is what our endpoint will return.

    Example response:
    {
        "message": "Machine learning is a type of AI..."
    }
    """
    message: str