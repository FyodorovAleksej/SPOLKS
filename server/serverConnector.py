import logging
import socket


class ServerConnector:
    def __init__(self, port, hostname, max_size, max_queue):
        """
        initialize connector by port, hostname and maximum size of bytes to send
        ========================================================================
        :param port: number of port for connect
        :param hostname: host to connect
        :param max_size: maximum size of bytes per one send
        :param max_size: maximum clients in queue
        """

        self.__LOGGER = logging.getLogger(ServerConnector.__name__)
        self.__port = port
        self.__hostname = hostname
        self.__sock = socket.socket()
        self.__max_size = max_size
        self.__max_queue = max_queue
        self.__current_conn = None
        self.__current_addr = None
        self.__connections = {}

    def get_current_conn(self):
        return self.__current_conn

    def start(self):
        self.__sock.bind((self.__hostname, self.__port))
        self.__LOGGER.info("server was started")
        self.__sock.listen(self.__max_queue)

    def accept(self):
        conn, addr = self.__sock.accept()
        self.__LOGGER.info("client was connected (" + str(conn) + ", " + str(addr) + ")")
        self.__current_conn = conn
        self.__current_addr = addr
        return conn, addr

    def send(self, byte_array):
        """
        send bytes to host by socket with settled max size
        ==================================================
        :param byte_array: bytes to send
        :return: is sending complete successfully?
        """
        if self.__current_conn is None:
            self.__LOGGER.warning("connection wasn't established")
            raise ConnectionAbortedError("connection don't established")
        while len(byte_array) > 0:
            sends = self.__current_conn.send(byte_array[:self.__max_size])
            byte_array = byte_array[sends:]
        return True

    def set_timeout(self, timeout):
        self.__sock.settimeout(timeout)
        self.__LOGGER.info("timeout of socket is settled to " + str(timeout))
        if self.__current_conn is not None:
            self.__LOGGER.info("timeout of connect socket is settled to " + str(timeout))
            self.__current_conn.settimeout(timeout)

    def receive(self):
        """
        receive answer from server with settled max size of bytes
        =========================================================
        :return: answer from server
        """
        if self.__current_conn is None:
            self.__LOGGER.warning("connection don't established")
            raise ConnectionAbortedError("connection don't established")
        return self.__current_conn.recv(self.__max_size).decode()

    def close(self):
        """
        close connection
        :return: None - always
        """
        if self.__current_conn is not None:
            self.__current_conn.close()
        self.__sock.close()
        self.__LOGGER.info("closing connection.")
