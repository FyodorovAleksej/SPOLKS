import socket


def receive_file(server_connector, destination_path, old_data):
    print("receive = " + old_data)
    file_destination = open(destination_path, "w")
    if file_destination:
        server_connector.set_timeout(1.0)
        file_destination.write(old_data)
        while True:
            try:
                data = server_connector.receive()
                print("receive = " + data)
                file_destination.write(data)
            except socket.timeout:
                server_connector.set_timeout(None)
                break
    file_destination.flush()
    file_destination.close()


def send_file(server_connector, source_path, partition_size):
    file_source = open(source_path, "r")
    if file_source:
        while True:
            buffer = file_source.read(partition_size)
            print("read : " + buffer)
            if buffer is not "":
                server_connector.send(buffer.encode())
            else:
                break
