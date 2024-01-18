# FROM python:3.9-alpine

# WORKDIR /opt/app

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8000

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# CMD ["gunicorn", "eVDR.wsgi:application", "--bind", "0.0.0.0:8000"]

# Use python:3.9-alpine as the base image
FROM python:3.9-alpine

# Set the working directory to /opt/app
WORKDIR /opt/app

# Copy the requirements file into the image
COPY requirements.txt .

# Update the package list and install Rust and Cargo
RUN apk update \
    && apk add --no-cache rust cargo

# Optional: Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install the Python dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy the rest of your application's code into the image
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Set environment variables to prevent Python from writing .pyc files to disc
# and to prevent Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define the command to run your application
CMD ["gunicorn", "eVDR.wsgi:application", "--bind", "0.0.0.0:8000"]
