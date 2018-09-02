#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import socket

from configobj import ConfigObj

from server.parser.serverParser import ServerParser, split_lines
from server.serverConnector import ServerConnector
import commonFileLib

# Logging settings
logging.basicConfig(handlers=[
    logging.FileHandler(u"serverLog.log"),
    logging.StreamHandler()
], format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

# Path to properties file
SERVER_PROPERTIES_FILE = "./resources/serverconfig.ini"

# Keys to properties file
# Number of port to connect
SERVER_PORT_KEY = "default_port"
# Max size to send/receive
SERVER_SIZE_KEY = "default_size"
# Host of socket
SERVER_HOST_KEY = "server_host"
# Max count of connections in socket queue
SERVER_QUEUE_KEY = "server_queue"

# Config
config = ConfigObj(SERVER_PROPERTIES_FILE)

# Reading config
DEFAULT_PORT = int(config[SERVER_PORT_KEY])
DEFAULT_HOST = config[SERVER_HOST_KEY]
DEFAULT_SIZE = int(config[SERVER_SIZE_KEY])
DEFAULT_QUEUE = int(config[SERVER_QUEUE_KEY])

serverConnector = ServerConnector(DEFAULT_PORT, DEFAULT_HOST, DEFAULT_SIZE, DEFAULT_QUEUE)

if __name__ == "__main__":
    try:
        serverConnector.start()

        running = True
        while running:
            serverConnector.set_timeout(1000)
            serverConnector.accept()
            server_parser = ServerParser(serverConnector.get_current_conn())

            while running:
                data = serverConnector.receive()
                serverConnector.set_timeout(1.0)
                while True:
                    try:
                        data += serverConnector.receive()
                    except socket.timeout:
                        serverConnector.set_timeout(None)
                        break

                print("getting data = " + data)
                if not data:
                    print("nothing to read")
                    break
                lines = split_lines(data)
                response = ""
                for i in range(0, len(lines)):
                    print("performing command \"" + str(lines[i]) + "\" ...")
                    command, param = server_parser.parse_command(lines[i])
                    if command is not None:
                        if command.is_exit_command():
                            command.perform_command(param)
                            serverConnector.close()
                            running = False
                            break
                        if command.is_upload_command():
                            oldData = ""
                            for j in range(i + 1, len(lines)):
                                oldData += lines[j] + "\n"
                            speed = commonFileLib.receive_file(serverConnector, command.perform_command(param), oldData)
                            response = str(speed)
                            print("speed = " + response)
                            i = len(lines)
                            lines = []
                            break
                        if command.is_download_command():
                            speed = commonFileLib.send_file(serverConnector, command.perform_command(param), DEFAULT_SIZE)
                            response = str(speed)
                            print("speed = " + response)
                            break
                        if param is not None:
                            response += command.perform_command(param)
                    else:
                        print("invalid command")
                print("responsing : " + response)
                if running:
                    serverConnector.send(response.encode())
    finally:
        serverConnector.close()
