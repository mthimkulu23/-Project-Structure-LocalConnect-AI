from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

# --- START TEMPORARY DEBUGGING LINES ---
groq_key_val = os.getenv("GROQ_API_KEY")
if groq_key_val:
    print(f"DEBUG: GROQ_API_KEY loaded successfully. Starts with: {groq_key_val[:5]}...")
else:
    print("ERROR: GROQ_API_KEY is NOT set in environment variables!")
    # Optionally, you can add a sys.exit(1) here if you want to force it to fail
    # if the key is missing, making the error more explicit.
    # import sys
    # sys.exit(1)
# --- END TEMPORARY DEBUGGING LINES ---


from app.api import router as api_router

app = FastAPI(
    title="LocalConnect AI API",
    description="API for LocalConnect AI chatbot to find local services.",
    version="1.0.0",
)

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