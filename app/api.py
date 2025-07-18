from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.chatbot import LocalConnectChatbot
from app.utils import load_env_variables
import json # Import json to help with logging if needed, though direct print might be enough for a string response

# Initialize API Router
router = APIRouter()

# Load environment variables
load_env_variables()

# Initialize the chatbot (this will load LLMs and service managers)
# Ensure this is done once and accessible to your routes
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
    location = query_data.get("location", "current_location") # Default to current location

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        response = await chatbot.process_query(query, location)

        # --- ADD THESE DEBUGGING LINES ---
        print(f"DEBUG: FastAPI is about to return response: '{response}'")
        print(f"DEBUG: Type of response: {type(response)}")
        # If 'response' is not a string, you might want to try:
        # print(f"DEBUG: FastAPI is about to return response (JSON dumped): {json.dumps({'response': response})}")
        # ---------------------------------

        return {"response": response}
    except Exception as e:
        # Log the detailed error for debugging purposes (e.g., in FastAPI console)
        print(f"Error processing query in API endpoint: {e}") # Clarified log message
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")