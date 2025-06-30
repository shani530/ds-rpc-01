from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ChatRequest, ChatResponse

from app.services.rag import query_repository  # Import the RAG service function
from app.utils.util import authenticate  # Import the authenticate function from utils

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def query(
    chat_request: ChatRequest
): 
    """
    Chat endpoint with RAG functionality
    """

    query_response = query_repository(
        query = chat_request.message,
        user_role=chat_request.role
    )

    return ChatResponse(
        answer= query_response['response'],
        source="placeholder_document.md"
    )
