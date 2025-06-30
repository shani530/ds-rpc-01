#!/usr/bin/env python3
"""
Simple debug server for FastAPI
This script makes it easier to debug your FastAPI application
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting FastAPI Debug Server...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("📖 API Documentation: http://127.0.0.1:8000/docs")
    print("🔧 Debug mode enabled - breakpoints will work!")
    
    uvicorn.run(
        "app.main:app",  # Use import string instead of app object
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug"
    )
