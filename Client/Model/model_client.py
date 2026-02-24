import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.max_message_size = 1024

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send(self, text):
        self.socket.send(text.encode())

    def receive(self):
        data = self.socket.recv(self.max_message_size)

        if data == b"":
            return "_offline_"

        return data.decode()