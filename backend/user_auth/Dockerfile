# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./auth.py .

# Expose the port the Flask app runs on
EXPOSE 5001

ENV FLASK_APP=auth.py

CMD ["python", "auth.py"]