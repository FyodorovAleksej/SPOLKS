import socket


# Class of connection to host by socket
class ClientConnector:
    def __init__(self, port, hostname, max_size):
        """
        initialize connector by port, hostname and maximum size of bytes to send
        ========================================================================
        :param port: number of port for connect
        :param hostname: host to connect
        :param max_size: maximum size of bytes per one send
        """
        self.__port = port
        self.__hostname = hostname
        self.__sock = socket.socket()
        self.__max_size = max_size

    def set_port(self, port):
        """
        setting current port
        ====================
        :param port: new number of port
        :return: None - always
        """
        self.__port = port

    def connect(self):
        """
        connect to settled host by port
        ===============================
        :return: result of connection
        """
        try:
            self.__sock.connect((self.__hostname, self.__port))
            return True
        except OSError:
            self.__sock.close()
            self.__sock = socket.socket()
            return False

    def send(self, byte_array):
        """
        send bytes to host by socket with settled max size
        ==================================================
        :param byte_array: bytes to send
        :return: is sending complete successfully?
        """
        while len(byte_array) > 0:
            sends = self.__sock.send(byte_array[:self.__max_size])
            byte_array = byte_array[sends:]
        return True

    def receive(self):
        """
        receive answer from server with settled max size of bytes
        =========================================================
        :return: answer from server
        """
        return self.__sock.recv(self.__max_size).decode()

    def close(self):
        """
        close connection
        :return: None - always
        """
        self.__sock.close()
