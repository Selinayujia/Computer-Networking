#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 18:25:15 2019

@author: selina
"""
import time
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1',12000)
try:
    for sequence_number in range (1, 11):
        print("-"*20)
        initial_time = time.time()
        display_time = time.asctime( time.localtime(time.time()) )
        client_socket.settimeout(1)
        message = 'PING ' + str(sequence_number) +" "+ display_time
        sent = client_socket.sendto(message.encode(), server_address)
        print('Sending: ', message)
        print('Waiting to receive')
        try:
            data, server = client_socket.recvfrom(1024)
            end_time = time.time()
            rtt = end_time - initial_time
            print('Received the ', sequence_number, ': ', data.decode())
            print('The RTT for PING #', sequence_number, " is ",rtt)
        except socket.timeout:
            print('#' ,sequence_number ,' Request timed out')
        
finally:
    print('closing socket')
    client_socket.close()