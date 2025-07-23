# Your existing Dockerfile content above...

# Stage 2: Runtime environment
FROM python:3.12-slim-bookworm

# Set the working directory in the container for the runtime stage
WORKDIR /app

# Copy the installed packages from the build stage
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/

# Copy the rest of your application code
COPY . .

# Set the command to run your FastAPI application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]