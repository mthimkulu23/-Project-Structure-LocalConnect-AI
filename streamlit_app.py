

import streamlit as st
import requests
import os
from dotenv import load_dotenv 


load_dotenv() 


st.set_page_config(
    page_title="LocalConnect AI Chat",
    page_icon="💬",
    layout="centered", 
    initial_sidebar_state="collapsed"
)


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


for message in st.session_state.messages:

    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me Anything,"):
  
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

 
    payload = {"query": prompt, "location": "current_location"}
  

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
            
                response = requests.post(f"{FASTAPI_BACKEND_URL}/api/query/", json=payload)
                response.raise_for_status() 
                chatbot_response = response.json().get("response", "I'm sorry, I couldn't process your request.")
            except requests.exceptions.ConnectionError:
                chatbot_response = "I'm sorry, I can't connect to the AI service right now. Please ensure the backend is running and accessible at `FASTAPI_BACKEND_URL`."
            except requests.exceptions.HTTPError as e:
                st.error(f"Error from API: {e}. Detail: {response.json().get('detail', 'No detail provided')}")
                chatbot_response = "An error occurred while processing your request. Please try again."
            except Exception as e:
                chatbot_response = f"An unexpected error occurred: {e}"

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