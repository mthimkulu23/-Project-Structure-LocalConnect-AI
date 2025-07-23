from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Keep this import
from dotenv import load_dotenv
import os

load_dotenv()

# Remove the temporary debug print line, it's no longer needed
# print("DEBUG: app/main.py is being executed.")

from app.api import router as api_router # Keep this import

app = FastAPI(
    title="LocalConnect AI API",
    description="API for LocalConnect AI chatbot to find local services.",
    version="1.0.0",
)

# ADD THIS SECTION FOR THE HEALTH CHECK
@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to LocalConnect AI API!"}