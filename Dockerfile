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

# --- START DEBUGGING LINES (MODIFIED AGAIN) ---
# Print the current PATH variable (keeping for sanity check)
RUN echo "Current PATH: $PATH"
# Attempt to locate the uvicorn executable using which (still expected to fail)
RUN which uvicorn || echo "uvicorn not found in PATH by 'which'. Proceeding with broader search..."
# NEW: Find uvicorn executable across the entire filesystem.
# We pipe stderr to stdout to catch any permission errors or other messages from 'find'.
RUN find / -type f -name "uvicorn" -executable -print 2>&1 || echo "Uvicorn executable not found anywhere as executable (even after full system search)."
# NEW: List the contents of the uvicorn package directory. This will confirm if the package itself is there.
# This should show the __init__.py, cli.py etc.
RUN ls -l /usr/local/lib/python3.12/site-packages/uvicorn/ || echo "Uvicorn Python package directory not found."
# --- END DEBUGGING LINES ---

# Set the command to run your FastAPI application with Uvicorn via sh -c
# We'll re-enable this after debugging 'uvicorn not found'
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]