from typing import Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.routers.chat_router import router as chat_router
from app.utils.util import authenticate


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/chat", tags=["chat"])

# Login endpoint
@app.post("/login")
def login(user=Depends(authenticate)):

    print(f"DEBUG: Login endpoint called for user: {user}")  # Add debug here
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}
