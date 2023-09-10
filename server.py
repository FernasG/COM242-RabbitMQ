from pika import BlockingConnection, ConnectionParameters

def hello(ch, method, properties, body):
    print(f"[x] Received {body}")

if __name__ == "__main__": 
    queues = ["hello"]
    connection = BlockingConnection(ConnectionParameters("rabbitmq", "5672"))
    channel = connection.channel()

    for queue in queues:
        channel.queue_declare(queue)
    
    channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=hello)

    print("[*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()