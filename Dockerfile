# Use the official Python image as the base image
FROM python:3.13.0a4-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN apt-get update
RUN apt-get install libjpeg-dev zlib1g-dev -y
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Start the Flask server
CMD ["python", "app.py"]

