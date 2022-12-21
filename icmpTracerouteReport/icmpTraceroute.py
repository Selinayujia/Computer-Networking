#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:00:33 2019

@author: selina
"""

from socket import *
import os
import sys
import struct
import time
import select
import binascii
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def checksum(string):
	csum = 0

	countTo = (len(string) // 2) * 2

	count = 0


	while count < countTo:

		thisVal = ord(string[count+1]) * 256 + ord(string[count])

		csum = csum + thisVal

		csum = csum & 0xffffffff

		count = count + 2


	if countTo < len(string):

		csum = csum + ord(string[len(string) - 1])

		csum = csum & 0xffffffff


	csum = (csum >> 16) + (csum & 0xffff)

	csum = csum + (csum >> 16)

	answer = ~csum

	answer = answer & 0xffff 

	answer = answer >> 8 | (answer << 8 & 0xff00)

	return answer

# In this function we make the checksum of our packet
# hint: see icmpPing lab
def build_packet():
# In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
# packet to be sent was made, secondly the checksum was appended to the header and
# then finally the complete packet was sent to the destination.
# Make the header in a similar way to the ping exercise.
# Append checksum to the header.
# Don’t send the packet yet , just return the final packet in this function.
# So the function ending should look like this
    myChecksum = 0
    
    ID = os.getpid() & 0xFFFF # Return the current process i
    
	# Make a dummy header with a 0 checksum

	# struct -- Interpret strings as packed binary data

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    data = struct.pack("d", time.time())

	# Calculate the checksum on the data and the dummy header.

    dd = "".join( chr(x) for x in header)+"".join( chr(x) for x in data)
	
    myChecksum = checksum(dd) 

	# Get the right checksum, and put in the header

    if sys.platform == 'darwin':

		# Convert 16-bit integers from host to network byte order

        myChecksum = htons(myChecksum) & 0xffff

    else:

        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    return packet
def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet() 
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    print(" * * * Request timed out.")
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    print(" * * * Request timed out.")
            except timeout:
                continue
            else:
            
                ICMP_Header = recvPacket[20:28] # the icmp header is right after , 8 bytes
                types, code, checksum, id_num, seq = struct.unpack('bbHHh', ICMP_Header) #b stands for signed char, H stanfs for short, h stands for unsign
                
                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" %(ttl, (timeReceived -t)*1000, addr[0]))
                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" %(ttl, (timeReceived-t)*1000, addr[0]))
                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d rtt=%.0f ms %s" %(ttl, (timeReceived - timeSent)*1000, addr[0]))
                    return
                else:
                    print("error")
                break
            finally:
                mySocket.close()
                
print("Printing the first target host: google.com")
get_route("google.com")

print("Printing the second target host: nytimes.com")
get_route("nytimes.com")

print("Printing the third target host: facebook.com")
get_route("facebook.com")

print("Printing the fourth target host: yahoo.com")
get_route("yahoo.com")

