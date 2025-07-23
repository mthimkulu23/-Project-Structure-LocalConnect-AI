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
# This ENV PATH line is good, but uvicorn isn't in /usr/local/bin, so we need to find its actual path.
ENV PATH="/usr/local/bin:$PATH"

# Set the working directory in the container for the runtime stage
WORKDIR /app

# Copy the installed packages from the build stage
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/

# Copy the rest of your application code
COPY . .

# --- START DEBUGGING LINES (MODIFIED) ---
# Print the current PATH variable (already confirmed, but keeping for completeness)
RUN echo "Current PATH: $PATH"
# Attempt to locate the uvicorn executable using which (expected to fail again, confirms our understanding)
RUN which uvicorn || echo "uvicorn not found in PATH by 'which', searching now..."
# NEW: Find uvicorn executable in common Python installation paths
RUN find /usr/local -type f -name "uvicorn" -executable -print || echo "Uvicorn executable not found in /usr/local tree."
# --- END DEBUGGING LINES ---

# Set the command to run your FastAPI application with Uvicorn via sh -c
# We'll re-enable this after debugging 'uvicorn not found'
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]