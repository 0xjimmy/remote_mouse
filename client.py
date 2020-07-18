#!/usr/bin/env python3
from socket import *
import json
import pyautogui

serverPort = 12345

while True:
    # 1. Configure server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen(1)
    print("waiting for client connecting...")
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
    print(connectionSocket.getsockopt(SOL_SOCKET, SO_KEEPALIVE))
    print("...connected.")
    serverSocket.close(
    )  # Destroy the server socket; we don't need it anymore since we are not accepting any connections beyond this point.

    # 2. communication routine
    while True:
        try:
            sentence = connectionSocket.recv(512).decode()
        except ConnectionResetError as e:
            print("Client connection closed")
            break
        if (len(sentence) == 0):  # close if client closed connection
            break
        else:
            message = str(sentence)
            data = json.loads(message)
            pyautogui.moveTo(data["x"], data["y"])
            print("Recived:", message)

    # 3. proper closure
    connectionSocket.shutdown(SHUT_RDWR)
    connectionSocket.close()
    print("connection closed.")
