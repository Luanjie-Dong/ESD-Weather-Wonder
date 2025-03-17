Building Docker Image
Docker Build:
Build the Docker image for the microservice:

bash
1. docker build -t location .

Docker Run:
Run the container with port mapping and environment variables:

bash
2. docker run -p 5002:5002 --env-file .env location