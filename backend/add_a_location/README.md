Building Docker Image
Docker Build:
Build the Docker image for the microservice:

bash
1. docker build -t add_a_location .

Docker Run:
Run the container with port mapping and environment variables:

bash
2. docker run --name add_a_location -p 5010:5010 add_a_location

