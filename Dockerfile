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
# Ensure /usr/local/bin is in PATH (standard, no need to change)
ENV PATH="/usr/local/bin:$PATH"

# Set the working directory in the container for the runtime stage
WORKDIR /app

# Copy the installed packages from the build stage
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/

# Copy the rest of your application code
COPY . .

# --- REMOVING DEBUGGING LINES ---
# These debugging lines are no longer needed as we've identified the root cause.
# RUN echo "Current PATH: $PATH"
# RUN which uvicorn || echo "uvicorn not found in PATH by 'which'. Proceeding with broader search..."
# RUN find / -type f -name "uvicorn" -executable -print 2>&1 || echo "Uvicorn executable not found anywhere as executable (even after full system search)."
# RUN ls -l /usr/local/lib/python3.12/site-packages/uvicorn/ || echo "Uvicorn Python package directory not found."
# --- END REMOVAL OF DEBUGGING LINES ---


# Set the command to run your FastAPI application with Uvicorn
# Use 'python -m uvicorn' to run uvicorn as a module
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]