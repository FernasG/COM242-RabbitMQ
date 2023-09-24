import uuid

from pika import BlockingConnection, ConnectionParameters, BasicProperties, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

class Client:
    def __init__(self) -> None:
        queues = ["text_message", "file_edit", "calc"]
        credentials = PlainCredentials("admin", "123456")
        self.connection = BlockingConnection(ConnectionParameters("localhost", "5672", credentials=credentials))
        self.channel = self.connection.channel()

        for queue in queues:
            self.channel.queue_declare(queue)

        queue_result = self.channel.queue_declare(queue="", exclusive=True)
        self.reply_queue = queue_result.method.queue

        self.channel.basic_consume(queue=self.reply_queue, on_message_callback=self.on_response, auto_ack=True)

        self.response = None
        self.correlation_id = None
    
    def on_response(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        if self.correlation_id == properties.correlation_id:
            self.response = body.decode()

    def text_message(self) -> dict:
        text = input("Escreva a sua mensagem: ")
        body = str({"text": text})
        return {"routing_key": "text_message", "body": body}

    def file_edit(self) -> dict:
        text = input("Escreva o texto: ")
        body = str({"text": text})
        return {"routing_key": "file_edit", "body": body}

    def calc(self) -> dict:
        x = int(input("Digite um número: "))
        y = int(input("Digite outro número: "))
        body = str({"x": x, "y": y})
        return {"routing_key": "calc", "body": body}
    
    def call(self, option: int):
        options_map = {"1": self.text_message, "2": self.file_edit, "3": self.calc}

        function = options_map.get(str(option), None)
        params = function()

        self.response = None
        self.correlation_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange="", properties=BasicProperties(reply_to=self.reply_queue, correlation_id=self.correlation_id), **params)
        self.connection.process_data_events(time_limit=None)
        return self.response

def menu() -> str:
    print("*=" * 20)
    print("Menu")
    print("1 - Responder uma mensagem")
    print("2 - Editar arquivo de text")
    print("3 - Calculo de uma função")
    print("9 - Sair")

    return input("Escolha uma das opções acima: ")


if __name__ == "__main__":
    client = Client()

    loop = True

    while loop:
        # os.system("clear")
        option = menu()

        if not option.isdigit(): continue

        option = int(option)

        if option not in [1, 2, 3]:
            print("Saindo...")
            loop = False
        
        response = client.call(option)
        print(response)

    # connection.close()
