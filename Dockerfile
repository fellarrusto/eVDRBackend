# Use the official Rust image based on Alpine
FROM rust:1.64.0-alpine3.16

# Install Python
RUN apk add --no-cache python3 py3-pip

# Set the working directory in the container
WORKDIR /opt/app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Command to run on container start
CMD ["gunicorn", "eVDR.wsgi:application", "--bind", "0.0.0.0:8000"]
