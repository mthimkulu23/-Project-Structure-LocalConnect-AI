# LocalConnectAI/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv # <--- ADD THIS LINE
import os # Make sure os is imported if not already

# Load environment variables at the very start of the FastAPI app
load_dotenv() # <--- ADD THIS LINE

from app.api import router as api_router

app = FastAPI(
    title="LocalConnect AI API",
    description="API for LocalConnect AI chatbot to find local services.",
    version="1.0.0",
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to LocalConnect AI API!"}