import socket
import sys

CONSTANTS = {"IP": "127.0.0.1", "PORT": 8080, "HEADER_LENGTH": 10}


def add_input(input_stack):
    while True:
        input_stack.append(sys.stdin.readline())


def cook_client_socket(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.setblocking(False)
    return client_socket


def cook_server_socket(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen()
    return server_socket
