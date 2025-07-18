from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.chatbot import LocalConnectChatbot
from app.utils import load_env_variables
import json 

# Initialize API Router
router = APIRouter()

# Load environment variables
load_env_variables()

# Initialize the chatbot (this will load LLMs and service managers)
chatbot_instance = LocalConnectChatbot()

# Dependency to get the chatbot instance
def get_chatbot():
    return chatbot_instance

@router.post("/query/")
async def query_chatbot(
    query_data: Dict[str, str],
    chatbot: LocalConnectChatbot = Depends(get_chatbot)
):
    """
    Processes a user query to find local services or answer general questions.
    """
    query = query_data.get("query")
    location = query_data.get("location", "current_location") 

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        response = await chatbot.process_query(query, location)

        # Debugging output to console
        print(f"DEBUG: FastAPI is about to return response: '{response}'")
        print(f"DEBUG: Type of response: {type(response)}")
        

        return {"response": response}
    except Exception as e:
        # Log the detailed error for debugging purposes (e.g., in FastAPI console)
        print(f"Error processing query in API endpoint: {e}") 
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")