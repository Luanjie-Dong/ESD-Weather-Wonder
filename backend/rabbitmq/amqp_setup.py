#!/usr/bin/env python3

"""
A standalone script to create exchanges and queues on RabbitMQ.
"""
from dotenv import load_dotenv
import pika
import os

# Load environment variables from .env file
load_dotenv()

amqp_host = os.getenv("AMQP_HOST", 'localhost')
amqp_port = int(os.getenv("AMQP_PORT", 5672))
exchange_name = os.getenv("EXCHANGE_NAME")
exchange_type = os.getenv("EXCHANGE_TYPE")
amqp_user = os.getenv("AMQP_USER")
amqp_pass = os.getenv("AMQP_PASS")

def create_exchange(hostname, port, exchange_name, exchange_type, username, password):
    print(f"Connecting to AMQP broker {hostname}:{port}...")
    # connect to the broker
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=hostname,
            port=port,
            credentials=credentials,
            heartbeat=300,
            blocked_connection_timeout=300,
        )
    )
    print("Connected")

    print("Open channel")
    channel = connection.channel()

    # Set up the exchange if the exchange doesn't exist
    print(f"Declare exchange: {exchange_name}")
    channel.exchange_declare(
        exchange=exchange_name, exchange_type=exchange_type, durable=True
    )
    # 'durable' makes the exchange survive broker restarts

    return connection, channel

def create_queue(channel, exchange_name, queue_name, routing_key, max_priority=10):
    print(f"Creating queue: {queue_name} with routing key: {routing_key}")
    args = {"x-max-priority": max_priority}
    channel.queue_declare(queue=queue_name, durable=True, arguments=args)
    # 'durable' makes the queue survive broker restarts

    # bind the queue to the exchange via the routing_key
    channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=routing_key
    )
    print(f"Queue {queue_name} created and bound to exchange {exchange_name} with routing key {routing_key}")

def main():
    connection, channel = create_exchange(
        hostname=amqp_host,
        port=amqp_port,
        exchange_name=exchange_name,
        exchange_type=exchange_type,
        username=amqp_user,
        password=amqp_pass
    )

    create_queue(
        channel=channel,
        exchange_name=exchange_name,
        queue_name="Notification",
        routing_key="#.notification",
        max_priority=10
    )

    create_queue(
        channel=channel,
        exchange_name=exchange_name,
        queue_name="Notification_Reply",
        routing_key="#.notification.reply",
    )

    create_queue(
        channel=channel,
        exchange_name=exchange_name,
        queue_name="Trigger_Forecast_Process",
        routing_key="#.update",
    )

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()