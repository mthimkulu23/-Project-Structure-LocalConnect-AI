import streamlit as st
import requests
import os
import time # Add this import for time.sleep in the retry logic
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Local Connect AI Chat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# It's good that you're using an environment variable for the URL
FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 2rem;
    }
    .css-1d391kg, .css-1dp5x6x {
        padding-top: 0rem;
    }
    .stChatInputContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background-color: white; /* Or a light grey */
        border-top: 1px solid #f0f2f6;
        z-index: 1000;
    }
    .stChatMessage {
        max-width: 80%; /* Constrain message width */
        margin-bottom: 0.5rem;
    }
    /* Custom styling for user messages */
    .stChatMessage.st-cc .st-ea { /* Targeting the user message container */
        background-color: #e0f2f0; /* Light green for user, or a custom blue */
        border-radius: 18px;
        padding: 10px 15px;
        align-self: flex-end; /* Align user messages to the right */
        margin-left: auto; /* Push to the right */
    }
    /* Custom styling for assistant messages */
    .stChatMessage.st-ce .st-ea { /* Targeting the assistant message container */
        background-color: #f0f2f6; /* Light grey for assistant */
        border-radius: 18px;
        padding: 10px 15px;
        align-self: flex-start; /* Align assistant messages to the left */
        margin-right: auto; /* Push to the left */
    }
    /* Profile picture/icon styling */
    .stChatMessage .st-da, .stChatMessage .st-dc {
        /* Adjust icon/avatar size or hide if not needed */
        width: 32px;
        height: 32px;
        border-radius: 50%;
        margin-top: 5px;
    }
    .stChatMessage .st-da { /* User avatar */
        order: 2; /* Move avatar to the right of text for user */
        margin-left: 10px;
    }
    .stChatMessage .st-dc { /* Assistant avatar */
        order: 1; /* Keep avatar to the left of text for assistant */
        margin-right: 10px;
    }
    .stChatMessage .st-ea { /* Message content */
        order: 1; /* Text comes before avatar for user, after for assistant */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("LocalConnect AI Chat 💬")
st.markdown("Your intelligent assistant for discovering local services.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Custom API Call Function with Retry Logic ---
def call_backend_api_with_retry(query, location, retries=5, delay=5):
    for i in range(retries):
        try:
            response = requests.post(f"{FASTAPI_BACKEND_URL}/api/query/", json={"query": query, "location_info": location})
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            # --- IMPORTANT FIX HERE: Use response.text directly ---
            # Your FastAPI backend is returning a plain string, not a JSON object
            return response.text 
            # If your FastAPI *was* returning JSON like {"response": "Hi!"},
            # you would use: return response.json().get('response', 'No response provided.')
            # But based on your logs, it's a plain string.
            # --- END IMPORTANT FIX ---

        except requests.exceptions.ConnectionError:
            st.warning(f"Attempt {i+1}/{retries}: Connection to backend failed. Retrying in {delay} seconds...")
            time.sleep(delay)
        except requests.exceptions.Timeout:
            st.warning(f"Attempt {i+1}/{retries}: Backend request timed out. Retrying in {delay} seconds...")
            time.sleep(delay)
        except requests.exceptions.HTTPError as e:
            # For HTTP errors, try to get more detail if available
            error_detail_text = response.text if response else "No detailed error message provided."
            st.error(f"API Error: {e}. Detail: {error_detail_text}")
            # Do not retry on HTTPError unless it's specifically a 50x error you want to retry
            return None # Or raise the exception to stop further processing
        except Exception as e:
            st.error(f"An unexpected error occurred during API call: {e}")
            return None # Stop processing on unexpected errors

    st.error("Failed to connect to the backend API after multiple retries. The service might be temporarily unavailable.")
    return None
# --- End Custom API Call Function ---


for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me Anything,"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Use the hardcoded location based on your previous messages
    # If you later implement dynamic location, replace this.
    current_location = "Katlehong, Gauteng, South Africa" 
    payload = {"query": prompt, "location_info": current_location} # Ensure the key matches your FastAPI expectation


    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            # Call your new retry function
            chatbot_response = call_backend_api_with_retry(prompt, current_location)
            
            if chatbot_response is None:
                # If call_backend_api_with_retry returned None, it means an error occurred
                # The st.error message would have already been shown by the function.
                # You might want a generic fallback message here or let the spinner just go away.
                chatbot_response = "I'm sorry, I couldn't get a response from the AI."

        st.markdown(chatbot_response)

    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})


st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; font-size: 0.8em; color: grey;">
        Powered by LocalConnect AI

    </div>
    """,
    unsafe_allow_html=True
)