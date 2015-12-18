# Echo client program
import socket
import sys
import time
import re

HOST = 'localhost'
PORT = 9009
s = None

CLIENT_NAME = 'eoghan'

ROOM_REF = '1'
JOIN_ID = '1'
CHATROOM_NAME = ''
SERVER_IP = ''
SERVER_PORT = ''

while 1:
    recieve = False

    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print ('could not open socket')
        sys.exit(1)

    command = input('Enter client command: ')
	
    s.sendall('JOIN_CHATROOM: ' + command + '\n')
    recieve = True

    if recieve == True:
        data = s.recv(1024)
        s.close()
        print(data)
    else:
        s.close()