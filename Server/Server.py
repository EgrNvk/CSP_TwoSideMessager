import socket
import threading

HOST = '127.0.0.1'
PORT = 4000

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server_socket = None
        self.max_message_size = 1024

        self.clients = {}      # {id: socket}
        self.client_counter = 0

        self.running = False
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.running = True

        threading.Thread(target=self.accept_clients, daemon=True).start()
        print("Server _started_")

    def accept_clients(self):
        while self.running:
            try:
                conn, addr = self.server_socket.accept()

                with self.lock:
                    self.client_counter += 1
                    client_id = self.client_counter
                    self.clients[client_id] = conn

                print(f"Client {client_id} connected from {addr}")

                conn.send(f"ID:{client_id}".encode())

                threading.Thread(target=self.process_client,args=(client_id,),daemon=True).start()

            except:
                break

    def process_client(self, client_id):
        while self.running:
            try:
                with self.lock:
                    if client_id not in self.clients:
                        break
                    conn = self.clients[client_id]

                data = conn.recv(self.max_message_size)

                if not data:
                    break

                message = data.decode().strip()

                if message == "EXIT":
                    print(f"Client {client_id} requested exit")
                    break

                print(f"Client {client_id}: {message}")

            except:
                break

        self.remove_client(client_id)

    def send(self, client_id, text):
        with self.lock:
            if client_id in self.clients:
                try:
                    self.clients[client_id].send(text.encode())
                except:
                    self.remove_client(client_id)

    def remove_client(self, client_id):
        with self.lock:
            conn=self.clients.pop(client_id, None)
        if not conn:
            return

        try:
            conn.sendall(b"_offline_")
        except:
            pass

        try:
            conn.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            conn.close()
        except:
            pass

        print(f"Client {client_id} _removed_")

    def stop(self):
        self.running = False

        with self.lock:
            ids = list(self.clients.keys())

        for client_id in ids:
            self.remove_client(client_id)

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

        print("Server _stopped_")

server = Server(HOST, PORT)
server.start()

try:
    while True:
        line = input().strip()

        if not line:
            continue

        if line.lower() == "_exit_":
            break

        parts = line.split(":", 1)
        if len(parts) < 2 or not parts[0].isdigit():
            print("Формат: <id>:<повідомлення>")
            continue

        client_id = int(parts[0])
        text = parts[1]

        server.send(client_id, text)

except KeyboardInterrupt:
    pass

server.stop()