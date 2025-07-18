
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv 
import os 

load_dotenv() 

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