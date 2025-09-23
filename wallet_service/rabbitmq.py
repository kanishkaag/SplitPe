import pika
import json
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

def consume_wallet_credit(callback):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="wallet.credit.requested", durable=True)

    def on_message(ch, method, properties, body):
        message = json.loads(body)
        callback(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="wallet.credit.requested", on_message_callback=on_message)
    print(" Listening on queue: wallet.credit.requested")
    channel.start_consuming()
