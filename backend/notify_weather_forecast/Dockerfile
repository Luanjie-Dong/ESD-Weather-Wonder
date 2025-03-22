# Base image with Python
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside the container
WORKDIR /app

# Install system dependencies (optional: for network requests, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./notify_weather_forecast.py .
COPY ./amqp_lib.py .

# Expose the port the Flask app runs on
EXPOSE 5020

ENV FLASK_APP=notify_weather_forecast.py

# Run the Flask app
CMD ["python", "-u", "notify_weather_forecast.py"]