import socket
import threading
import time


class Server:
    __instance = None

    @staticmethod
    def get_instance():
        if not Server.__instance:
            Server()
        return Server.__instance

    def __init__(self):
        if Server.__instance:
            raise Exception("Singleton")
        else:
            Server.__instance = self

        self.host = '0.0.0.0'
        self.port = 9999
        self.server_socket = None
        self.clients = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            client_name = client_socket.recv(1024).decode()
            print(f"{client_name} conectado no ip {address}")
            self.clients.append({"socket": client_socket, "nome": client_name})
            client_thread = threading.Thread(target=self.handle_client_messages, args=(client_socket, client_name))
            client_thread.start()
            self.broadcast_message(f"{client_name} conectado no ip {address}", "SERVIDOR")

    def handle_client_messages(self, client_socket, client_name):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    self.broadcast_message(message, client_name)
            except:
                self.remove_client(client_socket, client_name)
                break

    def broadcast_message(self, message, sender_name):
        for client in self.clients:
            client_socket = client['socket']
            timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            text = f"{timestamp} - {sender_name}: {message}"  
                      
            try:
                client_socket.send(text.encode())
                print(f"{sender_name} : {message}")
            except:
                self.remove_client(client_socket, client['name'])

    def remove_client(self, client_socket, client_name):
        for client in self.clients:
            if client['socket'] == client_socket:
                self.clients.remove(client)
                print(f"{client_name} desconectado")
                break


if __name__ == "__main__":
    Server().get_instance().start()
