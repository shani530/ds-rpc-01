from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    role: str  # User's role, e.g., "engineering", "marketing", etc.

class ChatResponse(BaseModel):
    answer: str
    source: str  # Reference to the document or section