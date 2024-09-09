# Use an official Python runtime as the base image
FROM python:3.10.6-buster

# Install necessary dependencies for OpenCV and other system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the application code to the container
COPY fast.py fast.py
COPY requirements.txt requirements.txt

ENV PORT = 8000


# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

# Specify the command to run the application
CMD uvicorn fast:app --host 0.0.0.0 --port $PORT
