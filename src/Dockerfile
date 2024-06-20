# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    dos2unix

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's source code into the container
COPY . .

# Ensure the scripts have Unix-style line endings and are executable
RUN dos2unix ./run_pipeline.sh && chmod +x ./run_pipeline.sh

# Run the application
ENTRYPOINT ["./run_pipeline.sh"]
