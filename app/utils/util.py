from typing import Dict
from fastapi import HTTPException, Depends 
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"}
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username  # <- Set breakpoint here
    password = credentials.password
    
    # Debug prints with flush
    print(f"🔍 DEBUG: Received username: '{username}'", flush=True)
    print(f"🔍 DEBUG: Received password: '{password}'", flush=True)
    print(f"🔍 DEBUG: Available users: {list(users_db.keys())}", flush=True)
    
    user = users_db.get(username)  # <- Or set breakpoint here
    print(f"🔍 DEBUG: Found user: {user}", flush=True)
    
    if not user or user["password"] != password:
        print(f"❌ DEBUG: Authentication failed - User exists: {user is not None}, Password match: {user['password'] == password if user else False}", flush=True)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    print(f"✅ DEBUG: Authentication successful for user: {username}", flush=True)
    return {"username": username, "role": user["role"]}