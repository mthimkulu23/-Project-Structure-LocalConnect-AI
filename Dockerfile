# Your existing Dockerfile content above...

# Stage 2: Runtime environment
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the installed packages from the build stage
COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/

# Copy the rest of your application code
COPY . .

# Temporarily change CMD to just run the Python script to see print statements
CMD ["python", "app/main.py"]