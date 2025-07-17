from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.chatbot import LocalConnectChatbot # <--- Uncomment this
from app.utils import load_env_variables # <--- Uncomment this

# Initialize API Router
router = APIRouter() 

# Load environment variables
load_env_variables() # <--- Uncomment this

# Initialize the chatbot (this will load LLMs and service managers)
# Ensure this is done once and accessible to your routes
chatbot_instance = LocalConnectChatbot() # <--- Uncomment this

# Dependency to get the chatbot instance
def get_chatbot():
    return chatbot_instance

@router.post("/query/")
async def query_chatbot(
    query_data: Dict[str, str],
    chatbot: LocalConnectChatbot = Depends(get_chatbot) # <--- Uncomment this
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
        return {"response": response}
    except Exception as e:
        # Log the detailed error for debugging purposes (e.g., in FastAPI console)
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")