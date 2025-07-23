# --- Stage 1: Build Environment ---
# Use a full Python image to install dependencies
FROM python:3.12-slim-buster AS build-env

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
FROM python:3.12-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory
WORKDIR /app

# Copy installed packages from the build-env stage
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/

# Copy the rest of your application code
COPY . .

# Expose the port your FastAPI app will listen on
EXPOSE 8000

# Command to run your FastAPI application
# Ensure app.main:app matches your main FastAPI application entry point
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

