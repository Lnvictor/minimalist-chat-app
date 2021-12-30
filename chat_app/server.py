import socket
import select

from utils import cook_server_socket, CONSTANTS


class ChatServer():
    def __init__(self, socket):
        self.socket = socket
        self.sockets_list = [socket]
        self.clients = {}


    def receive_message(self, client_socket):
        try:
            header_length = CONSTANTS["HEADER_LENGTH"]
            message_header = client_socket.recv(header_length)
            if not len(message_header):
                return False

            message_length = int(message_header.decode("utf-8").strip())
            return {"header": message_header, "data": client_socket.recv(2000)}

        except:
            return False

    def start(self):
        while True:
            read_sockets, _, exception_socktes = select.select(self.sockets_list, [], self.sockets_list)

            for notified_socket in read_sockets:
                if notified_socket == self.socket:
                    client_socket, client_address = self.socket.accept()
                    user = self.receive_message(client_socket)

                    if user is False:
                        continue

                    self.sockets_list.append(client_socket)
                    self.clients[client_socket] = user
                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                else:
                    message = self.receive_message(notified_socket)
                    
                    if message is False:
                        print('Closed connection from: {}'.format(self.clients[notified_socket]['data'].decode('utf-8')))
                        self.sockets_list.remove(notified_socket)
                        del self.clients[notified_socket]
                        continue
                        
                    user = self.clients[notified_socket]
                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

                    for client_socket in self.clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


if __name__ == "__main__":
    socket = cook_server_socket(CONSTANTS["IP"], CONSTANTS["PORT"])
    server = ChatServer(socket)
    server.start()

