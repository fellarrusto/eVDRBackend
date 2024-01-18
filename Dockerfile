# FROM python:3.9-alpine

# WORKDIR /opt/app

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8000

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# CMD ["gunicorn", "eVDR.wsgi:application", "--bind", "0.0.0.0:8000"]

# Start with a Rust base image
FROM rust:latest

# Set the working directory in the Docker image
WORKDIR /opt/app

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a symbolic link for python3 and pip3
RUN ln -s /usr/bin/python3 /usr/local/bin/python \
    && ln -s /usr/bin/pip3 /usr/local/bin/pip

# Copy the requirements file into the Docker image
COPY requirements.txt .

# Install the Python dependencies from the requirements file
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of your application's code into the Docker image
COPY . .

# Expose port 8000 to the outside world
EXPOSE 8000

# Set environment variables to prevent Python from writing .pyc files to disk
# and to prevent Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define the command to run the application
CMD ["gunicorn", "eVDR.wsgi:application", "--bind", "0.0.0.0:8000"]
