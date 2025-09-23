import pika
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")

def publish_message(message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue="order.recorded", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="order.recorded",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
    )

    connection.close()
