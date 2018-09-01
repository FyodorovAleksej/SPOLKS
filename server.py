#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

from configobj import ConfigObj
from serverParser import ServerParser, split_lines

SERVER_PROPERTIES_FILE = "./resources/serverconfig.ini"

SERVER_PORT_KEY = "default_port"
SERVER_SIZE_KEY = "default_size"
SERVER_HOST_KEY = "server_host"
SERVER_QUEUE_KEY = "server_queue"

config = ConfigObj(SERVER_PROPERTIES_FILE)

DEFAULT_PORT = int(config[SERVER_PORT_KEY])
DEFAULT_HOST = config[SERVER_HOST_KEY]
DEFAULT_SIZE = int(config[SERVER_SIZE_KEY])
DEFAULT_QUEUE = int(config[SERVER_QUEUE_KEY])

sock = socket.socket()
sock.bind((DEFAULT_HOST, DEFAULT_PORT))
print("server was started")
sock.listen(DEFAULT_QUEUE)

conn, addr = sock.accept()
print('connected:', addr)

server_parser = ServerParser(conn)
try:
    while True:
        data = conn.recv(DEFAULT_SIZE).decode()
        print("getting data = " + data)
        if not data:
            print("nothing to read")
            break
        lines = split_lines(data)
        response = ""
        for line in lines:
            print("performing command \"" + str(line) + "\" ...")
            current_response = server_parser.parse_command(line)
            if current_response is not None:
                response += current_response
            else:
                raise AttributeError("Invalid command")
        print("responsing : " + response)
        conn.send(response.encode())
finally:
    conn.close()
