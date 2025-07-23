# Stage 1: Build environment
FROM python:3.12-slim-bookworm AS build-env

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container for the build stage
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.12-slim-bookworm

# Set environment variables for runtime
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Add /usr/local/bin to PATH where Python executables are typically installed
ENV PATH="/usr/local/bin:$PATH"

# Set the working directory in the container for the runtime stage
WORKDIR /app

# Copy the installed packages from the build stage
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/

# Copy the rest of your application code
COPY . .

# Set the command to run your FastAPI application with Uvicorn via sh -c
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]