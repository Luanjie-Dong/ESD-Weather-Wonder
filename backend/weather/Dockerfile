# Use an official JDK runtime as a parent image
FROM eclipse-temurin:21-jdk

# Set the working directory inside the container
WORKDIR /

# Copy the built JAR file into the container
COPY target/wrapper-0.0.1-SNAPSHOT.jar wrapper-0.0.1-SNAPSHOT.jar

# Copy the .env file to the working directory
COPY src/main/resources/.env .env

# Expose the application port
EXPOSE 8081

# Run the application
CMD ["java", "-jar", "wrapper-0.0.1-SNAPSHOT.jar"]