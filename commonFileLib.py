import socket
import time


def receive_file(server_connector, destination_path, old_data):
    destination_path = str(destination_path)
    print("receive = " + old_data)
    total_size = 0
    start_time = time.time()
    file_destination = open(destination_path, "w")
    if file_destination:
        server_connector.set_timeout(1.0)
        file_destination.write(old_data)
        total_size = len(old_data)
        while True:
            try:
                data = server_connector.receive()
                print("receive = " + data)
                file_destination.write(data)
                total_size += len(data)
            except socket.timeout:
                server_connector.set_timeout(None)
                break
    file_destination.flush()
    file_destination.close()
    return total_size / (time.time() - start_time)


def send_file(server_connector, source_path, partition_size):
    file_source = open(source_path, "r")
    total_size = 0
    start_time = time.time()
    if file_source:
        while True:
            buffer = file_source.read(partition_size)
            if buffer is not "":
                success = server_connector.send(buffer.encode())
                total_size += success * partition_size
            else:
                break
    return total_size / (time.time() - start_time)
