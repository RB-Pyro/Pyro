# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install PyQt5
RUN pip install --no-cache-dir PyQt5

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run an interactive shell (this can be changed to run your application script)
CMD ["python"]
