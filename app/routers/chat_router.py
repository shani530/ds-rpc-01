from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ChatRequest, ChatResponse

from app.services.chat_service import ChatService  # Import the RAG service function
from app.utils.util import authenticate  # Import the authenticate function from utils

router = APIRouter()

# Create service instance
chat_service = ChatService()

@router.post("/", response_model=ChatResponse)
def query_chat(chat_request: ChatRequest, user=Depends(authenticate)): 
    """Handle chat queries with role-based authentication"""
    try:
        query_response = chat_service.query_repository(
            query=chat_request.message,
            user_role=chat_request.role
        )

        return ChatResponse(
            answer=query_response['response'],
            source=""
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


