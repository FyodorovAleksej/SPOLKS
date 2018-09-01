import socket


class ClientConnector:
    def __init__(self, port, hostname, max_size):
        self.__port = port
        self.__hostname = hostname
        self.__sock = socket.socket()
        self.__max_size = max_size

    def set_port(self, port):
        self.__port = port

    def connect(self):
        return self.__sock.connect((self.__hostname, self.__port))

    def send(self, byte_array):
        while len(byte_array) > 0:
            sends = self.__sock.send(byte_array[:self.__max_size])
            byte_array = byte_array[sends:]
        return True

    def receive(self):
        return self.__sock.recv(self.__max_size).decode()

    def close(self):
        self.__sock.close()
