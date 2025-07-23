
FROM python:3.10-slim-buster AS build-env

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first to leverage Docker's build cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Production Environment ---
# Use a much smaller image for the final application
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /app


COPY --from=build-env /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages/

# Copy the rest of your application code
COPY . .

# Expose the port your FastAPI app will listen on
EXPOSE 8000

# Command to run your FastAPI application
# Ensure app.main:app matches your main FastAPI application entry point
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Streamlit Frontend Dockerfile (Optional, if you deploy it separately with Docker) ---
# If your Streamlit app is a separate Render service, you'd use a similar Dockerfile for it.
# FROM python:3.10-slim-buster
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 8501 # Default Streamlit port
# CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]