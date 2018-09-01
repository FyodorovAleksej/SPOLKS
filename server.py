#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.bind(('', 9080))
print("server was started")
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(1024).decode()
    print("getting data = " + data)
    if not data:
        break
    conn.send(data.upper().encode())

conn.close()
