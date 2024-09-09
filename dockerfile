FROM python:3.10.6-buster

# Install necessary dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy your application files
COPY surf_buddy surf_buddy
COPY requirements.txt /requirements.txt

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set Python path to include surf_buddy module
ENV PYTHONPATH="/surf_buddy:${PYTHONPATH}"

# Set the command to run your application
CMD streamlit run surf_buddy/app/demo_app.py --server.port $PORT --server.headless true
