# Use the official CUDA base image
FROM nvidia/cuda:11.4.1-cudnn8-runtime-ubuntu20.04

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3-venv && \
    python3 -m venv venv && \
    /bin/bash -c "source venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt"

# Copy the Flask application code into the container at /app
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["/bin/bash", "-c", "source venv/bin/activate && flask run --host=0.0.0.0"]