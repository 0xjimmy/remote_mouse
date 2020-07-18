#!/usr/bin/env python3
import pyautogui
from socket import *
import time
import json

[screenWidth, screenHeight] = pyautogui.size()
mouseVX = -1

while True:
    # 1. configure socket dest.
    serverName = '127.0.0.1'
    serverPort = 12345
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        clientSocket.connect((serverName, serverPort))
        print(clientSocket.getsockopt(SOL_SOCKET, SO_KEEPALIVE))
    except ConnectionRefusedError as e:
        print("Server refused connection. retrying")
        time.sleep(1)
        continue

    # 2. communication routine
    while (1):
        [mouseX, mouseY] = pyautogui.position()
        if mouseX < (screenWidth - 2) and mouseVX > 0:
            mouseVX -= 1
            data = json.dumps({"x": mouseVX, "y": mouseY})
            try:
                clientSocket.send(bytes(data, "utf8"))
            except ConnectionResetError as e:
                print("Server connection closed")
                break
            pyautogui.moveTo(screenWidth - 2, mouseY)
        if mouseX > (screenWidth - 2):
            mouseVX += 1
            data = json.dumps({"x": mouseVX, "y": mouseY})
            try:
                clientSocket.send(bytes(data, "utf8"))
            except ConnectionResetError as e:
                print("Server connection closed")
                break
            pyautogui.moveTo(screenWidth - 2, mouseY)

    # 3. proper closure
    clientSocket.shutdown(SHUT_RDWR)
    clientSocket.close()
