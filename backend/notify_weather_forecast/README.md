# Building
docker build -t notify-weather-forecast-service .
docker run -p 6021:6021 --env-file .env notify-weather-forecast-service

# Note, the MS will keep retrying to connect to RabbitMQ, its normal to see
# errors for it to keep retrying, it should eventually connect and consume from queues

# run 'python producer_test.py' to test out this MS