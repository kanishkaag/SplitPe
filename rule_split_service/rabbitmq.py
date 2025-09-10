import pika
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")

def publish_wallet_credit(message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue="wallet.credit.requested", durable=True)

    channel.basic_publish(
        exchange="",
        routing_key="wallet.credit.requested",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()


def consume_order_recorded(callback):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue="order.recorded", durable=True)

    def on_message(ch, method, properties, body):
        message = json.loads(body)
        callback(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="order.recorded", on_message_callback=on_message)
    print(" [*] Waiting for messages in order.recorded")
    channel.start_consuming()
