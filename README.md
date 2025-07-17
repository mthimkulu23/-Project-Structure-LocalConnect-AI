
# LocalConnect AI

LocalConnect AI is a chatbot designed to help users discover local services such as restaurants, dentists, events, and more, using natural language queries.

## Features

* **Natural Language Understanding:** Understands user queries like "Police Station in Johannesburg" or "Top-rated dentists near me."
* **Service Discovery:** Integrates with external APIs (mocked for now, but expandable to Google Places, Yelp, etc.) to find relevant local services.
* **Conversational Interface:** Built with Streamlit for an interactive chat experience.
* **Scalable Backend:** Uses FastAPI for a robust and performant API.
* **AI Powered:** Leverages large language models (Hugging Face/OpenAI API) for enhanced conversational abilities and general knowledge.

## Technologies Used

* **Python**
* **FastAPI:** For building the RESTful API backend.
* **Streamlit:** For the interactive web-based chatbot frontend.
* **Hugging Face / OpenAI API:** For natural language processing and generation.
* **`python-dotenv`:** For managing environment variables securely.
* **`requests`:** For making HTTP requests to external APIs.
* **`uvicorn`:** ASGI server for running FastAPI applications.

## Project Structure