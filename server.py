import ast

from pika import BlockingConnection, ConnectionParameters, BasicProperties
from pika.spec import Basic
from pika.adapters.blocking_connection import BlockingChannel


def text_message(channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    body = ast.literal_eval(body.decode())
    text = body.get("text", "")
    message = f"Olá, você digitou o texto: \"{text}\""

    channel.basic_publish(exchange="", routing_key=properties.reply_to, properties=BasicProperties(correlation_id=properties.correlation_id), body=message)
    channel.basic_ack(delivery_tag=method.delivery_tag)

def file_edit(channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    body = ast.literal_eval(body.decode())
    text = body.get("text", "")

    with open("text", "w") as file:
        file.write(text)

    message = f"Você escreveu \"{text}\" no arquivo text"
    channel.basic_publish(exchange="", routing_key=properties.reply_to, properties=BasicProperties(correlation_id=properties.correlation_id), body=message)
    channel.basic_ack(delivery_tag=method.delivery_tag)

def calc(channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    body = ast.literal_eval(body.decode())
    x = body.get("x", 0)
    y = body.get("y", 0)

    message = f"{x} + {y} = {x+y}\n{x} - {y} = {x-y}\n{x} / {y} = {x/y}\n{x} * {y} = {x*y}"

    channel.basic_publish(exchange="", routing_key=properties.reply_to, properties=BasicProperties(correlation_id=properties.correlation_id), body=message)
    channel.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__": 
    queues = ["text_message", "file_edit", "calc"]
    connection = BlockingConnection(ConnectionParameters("localhost", "5672"))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    for queue in queues:
        channel.queue_declare(queue)
    
    channel.basic_consume(queue="text_message", on_message_callback=text_message)
    channel.basic_consume(queue="file_edit", on_message_callback=file_edit)
    channel.basic_consume(queue="calc", on_message_callback=calc)

    print("[*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()