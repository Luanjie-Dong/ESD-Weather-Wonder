"""
Reusable AMQP-related functions

References:
https://pika.readthedocs.io/en/stable/_modules/pika/exceptions.html#ConnectionClosed
"""

import time
import pika


def connect(hostname, port, exchange_name, exchange_type, username=None, password=None, max_retries=12, retry_interval=5,):
     retries = 0

     # loop to retry connection up to 12 times
     # with a retry interval of 5 seconds
     while retries < max_retries:
          retries += 1
          try:
                print(f"Connecting to AMQP broker {hostname}:{port}...")
                # connect to the broker
                connection = pika.BlockingConnection(
                     pika.ConnectionParameters(
                          host=hostname,
                          port=port,
                          credentials=pika.PlainCredentials(username, password),
                          heartbeat=300,
                          blocked_connection_timeout=300,
                     )
                )
                print("Connected")

                print("Open channel")
                channel = connection.channel()

                # Check whether the exchange exists
                print(f"Check existence of exchange: {exchange_name}")
                channel.exchange_declare(
                     exchange=exchange_name,
                     exchange_type=exchange_type,
                     durable=True,
                     passive=False,
                )
                # passive=True: If exchange does not exist, raise an error.

                print("Connected")
                return connection, channel

          except pika.exceptions.ChannelClosedByBroker as exception:
                message = f"{exchange_type} exchange {exchange_name} not found."
                connection.close()
                raise Exception(message) from exception

          except pika.exceptions.AMQPConnectionError as exception:
                print(f"Failed to connect: {exception=}")
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)

     raise Exception(f"Max {max_retries} retries exceeded...")


def close(connection, channel):
     channel.close()
     connection.close()

def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True     
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        return False


def start_consuming(
     hostname, port, exchange_name, exchange_type, queue_name, callback, username=None, password=None,
     routing_key="#", queue_arguments=None
):
     while True:
          try:
                connection, channel = connect(
                     hostname=hostname,
                     port=port,
                     exchange_name=exchange_name,
                     exchange_type=exchange_type,
                     username=username,
                     password=password
                )

                channel.queue_declare(queue=queue_name, durable=True, arguments=queue_arguments)

                channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)


                print(f"Consuming from queue: {queue_name}")
                channel.basic_consume(
                     queue=queue_name, on_message_callback=callback, auto_ack=False
                )
                channel.start_consuming()

          except pika.exceptions.ChannelClosedByBroker as exception:
                message = f"Queue {queue_name} not found."
                connection.close()
                raise Exception(message) from exception

          except pika.exceptions.ConnectionClosedByBroker:
                print("Connection closed. Try to reconnect...")
                continue

          except KeyboardInterrupt:
                close(connection, channel)
                break

          # Other types of exception are passed on to caller to handle.
          # Most likely, system issue - RabbitMQ host overload.
