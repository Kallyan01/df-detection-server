# Use the official CUDA base image
FROM nvidia/cuda:12.4.0-devel-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

#Install system dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev cmake libgl1-mesa-glx libglib2.0-dev && \
    /bin/bash -c "pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt"

# Copy the Flask application code into the container at /app
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=run.py
ENV FLASK_ENV=prod

# Run the Flask application
CMD ["/bin/bash", "-c", "flask run --host=0.0.0.0 --port=5000 & celery -A celery_worker worker --loglevel=INFO -P eventlet"]
# CMD ["/bin/bash", "-c", "source venv/bin/activate && flask run --host=0.0.0.0"]

