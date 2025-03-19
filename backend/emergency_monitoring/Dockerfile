# Use an official JDK runtime as a parent image
FROM eclipse-temurin:21-jdk

# Set the working directory inside the container
WORKDIR /

# Copy the built JAR file into the container
COPY target/composite-0.0.1-SNAPSHOT.jar composite-0.0.1-SNAPSHOT.jar

# Copy the .env file to the working directory
COPY src/main/resources/.env .env

# Expose the application port
EXPOSE 8082

# Run the application
CMD ["java", "-jar", "composite-0.0.1-SNAPSHOT.jar"]