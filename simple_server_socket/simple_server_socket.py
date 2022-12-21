#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:35:32 2019

@author: selina
"""
from socket import *
import sys
import socket 
serverSocket = socket.socket(AF_INET, SOCK_STREAM)

host_name = socket.gethostname() 
host_ip = socket.gethostbyname(host_name)         
PORT = 6789

while True:    
    with serverSocket as s:
        print("Getting host IP, Host IP is ",host_ip )
        s.bind((host_ip, PORT))
        s.listen()
        print('Ready to serve...')
        connectionSocket, addr = s.accept()
        try: 
            message = connectionSocket.recv(1024)
            filename = message.split()[1].decode()
            f = open(filename[1:],"r") 
            outputdata = f.read()
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><h1>404 Not Found</h1></html>\r\n".encode())
            connectionSocket.close()
    serverSocket.close()
    sys.exit()
    
    