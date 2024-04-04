# Use the official CUDA base image
FROM nvidia/cuda:12.3.2-devel-ubi8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install system dependencies using yum (for UBI-based images)
RUN yum install -y python3 python3-pip python3-venv

# Create and activate the virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code into the container at /app
COPY . .

# Expose the port the Flask app runs on
EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
