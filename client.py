from pika import BlockingConnection, ConnectionParameters

if __name__ == "__main__": 
    queues = ["hello"]
    connection = BlockingConnection(ConnectionParameters("localhost", "5672"))
    channel = connection.channel()

    for queue in queues:
        channel.queue_declare(queue)
    
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print("[x] Sent 'Hello World!'")
    connection.close()