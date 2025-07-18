# LocalConnect AI

LocalConnect AI is an intelligent chatbot designed to help users discover local services such as restaurants, dentists, events, and more, using natural language queries. It provides a conversational interface to simplify finding information and connections within a local area.

## Features

* **Natural Language Understanding (NLU):** Capable of understanding complex user queries like "Police Station in Johannesburg" or "Top-rated dentists near me" to extract intent and entities.
* **AI-Powered Responses:** Leverages advanced large language models, specifically **Groq's Llama 3 models**, for generating conversational, context-aware, and informative responses, as well as general knowledge queries.
* **Service Discovery Integration:** Designed to integrate with external APIs (currently uses OpenCage for geocoding and a mocked interface for service searching for demonstration, but easily expandable to real-world services like Google Places, Yelp, etc. if billing is enabled for those services) to find and retrieve relevant local service information.
* **Interactive Conversational Interface:** Built with Streamlit to provide a user-friendly and real-time chat experience, mimicking a natural conversation flow.
* **Scalable Backend:** Utilizes FastAPI for a robust, high-performance, and easily scalable API to handle chatbot requests and integrate with AI models.

## Technologies Used

* **Python:** The core programming language for the entire project.
* **FastAPI:** A modern, fast (high-performance) web framework for building the RESTful API backend.
* **Streamlit:** An open-source app framework for quickly building and deploying interactive web applications, serving as the chatbot's frontend.
* **`langchain-groq`**: Python library for seamless integration with Groq's super-fast LLM inference API.
* **`python-dotenv`:** For securely managing environment variables (like API keys) during local development.
* **`requests`:** A fundamental HTTP library for making requests to external APIs (e.g., to the FastAPI backend from Streamlit, or to OpenCage Geocoding).
* **`uvicorn`:** An ultra-fast ASGI server, used to run the FastAPI application.
* **`langchain-core`**: Core abstractions for LangChain, providing fundamental building blocks for LLM applications.

## Project Structure

The project is organized into a modular structure to ensure maintainability and clear separation of concerns between the frontend, backend, and core logic:


## Getting Started

Follow these steps to set up and run LocalConnect AI on your local machine for development and testing.

### Prerequisites

* Python 3.9 or higher
* Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/mthimkulu23/-Project-Structure-LocalConnect-AI](https://github.com/mthimkulu23/-Project-Structure-LocalConnect-AI)
    cd -Project-Structure-LocalConnect-AI
    ```

2.  **Create and activate a virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.

    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    Install all required Python packages using pip.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a file named `.env` in the root directory of your project (e.g., `LocalConnect-AI/.env`). This file will store your sensitive API keys for local development.

    ```env
    # .env file content
    GROQ_API_KEY="gsk_YOUR_GROQ_API_KEY_HERE"
    # Example: GROQ_API_KEY="hbhhikiuhgvvtgvgt"
    
    OPENCAGE_API_KEY="YOUR_OPENCAGE_API_KEY_HERE"
    # Example: OPENCAGE_API_KEY="your_opencage_key_xyz"

    # The backend URL for the frontend when running locally
    FASTAPI_BACKEND_URL="http://localhost:8000"
    ```
    * **Get your Groq API Key:** Obtain this key from [Groq Console](https://console.groq.com/keys).
    * **Get your OpenCage Geocoding API Key:** Obtain this key from [OpenCage Geocoding](https://opencagedata.com/developers).

### Running the Application Locally

LocalConnect AI consists of two independently runnable components: a FastAPI backend and a Streamlit frontend. Both need to be running for the application to function locally.

1.  **Run the FastAPI Backend:**
    Open your first terminal window (and activate your virtual environment).
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be accessible at `http://0.0.0.0:8000`. The `--reload` flag will automatically restart the server on code changes.

2.  **Run the Streamlit Frontend:**
    Open a second terminal window (and activate your virtual environment).
    ```bash
    streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
    ```
    Your Streamlit app will typically open in your default web browser at `http://0.0.0.0:8501`.

## Usage

Once both the FastAPI backend and the Streamlit frontend are running:

1.  Navigate to the Streamlit app URL in your browser (e.g., `http://localhost:8501`).
2.  Type your natural language query into the chat input field at the bottom of the interface.
3.  Press `Enter` or click the send button.
4.  The chatbot will process your request, communicate with the AI model (Groq), and provide a relevant response, or an error message if an issue occurs.

## Contributing

We welcome contributions to LocalConnect AI! If you'd like to improve the chatbot, add new features, or fix bugs, please follow these guidelines:

1.  **Fork the repository** on GitHub.
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b fix/bug-description`.
3.  **Make your changes**, ensuring they adhere to the project's coding style.
4.  **Commit your changes** with a clear and concise message (e.g., `feat: Add new service integration for pharmacies`).
5.  **Push your branch** to your forked repository: `git push origin feature/your-feature-name`.
6.  **Open a Pull Request** against the `main` branch of the original repository, describing your changes in detail.

## License

This project is licensed under the MIT License. See the `LICENSE` file in the repository for more details.

## Contact
* **Thabang Mthimkulu**
* [https://github.com/mthimkulu23]
* [https://www.linkedin.com/in/thabang-mthimkulu-b27316241/]
* [https://thabang23portfolio.netlify.app/#certifications]