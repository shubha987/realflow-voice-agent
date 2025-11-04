from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import webhook
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
load_dotenv()

# Create necessary directories
Path("logs").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)

app = FastAPI(
    title="Realflow Voice Agent API",
    description="Inbound Commercial Real Estate AI Agent with Vapi",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhook.router, prefix="/api", tags=["Webhooks"])

@app.get("/")
async def root():
    return {
        "message": "Realflow Voice Agent API",
        "status": "running",
        "brokerage": os.getenv("BROKERAGE_NAME", "Your Brokerage")
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)