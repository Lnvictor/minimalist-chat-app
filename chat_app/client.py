import collections
import errno
import socket
import sys
import threading

from utils import CONSTANTS, add_input, cook_client_socket


class UserClient:
    def __init__(self, socket):
        self.socket = socket

    def __run_input_getter(self, input_stack):
        input_thread = threading.Thread(target=add_input, args=(input_stack,))
        input_thread.daemon = True
        input_thread.start()
        return input_stack

    def start(self):
        header_length = CONSTANTS["HEADER_LENGTH"]
        my_username = input("Username: ")
        username = my_username.encode("utf-8")
        username_header = f"{len(username):<{header_length}}".encode("utf-8")
        # client.socket = cook_client_socket(IP, PORT)
        self.socket.send(username_header + username)
        input_stack = collections.deque()
        self.__run_input_getter(input_stack)

        while True:
            if len(input_stack):
                message = input_stack.pop().encode("utf-8")
                message_header = f"{len(message):<{header_length}}".encode("utf-8")
                self.socket.send(message_header + message)

            try:
                while True:
                    username_header = self.socket.recv(header_length)

                    if not len(username_header):
                        print("Connection closed by the server")
                        sys.exit()

                    username_length = int(username_header.decode("utf-8").strip("\n "))
                    username = self.socket.recv(username_length).decode("utf-8")

                    message_header = self.socket.recv(header_length)
                    message_length = int(message_header.decode("utf-8").strip("\n "))
                    message = self.socket.recv(message_length).decode("utf-8")
                    print(f"{username} > {message}", end="")

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error: {}".format(str(e)))
                    sys.exit()
                continue

            except Exception as e:
                print("Reading error: ".format(str(e)))
                sys.exit()


if __name__ == "__main__":
    socket = cook_client_socket(CONSTANTS["IP"], CONSTANTS["PORT"])
    client = UserClient(socket)
    client.start()
