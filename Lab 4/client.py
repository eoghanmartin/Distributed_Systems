# Echo client program
import socket
import sys
import time
import re
import select

HOST = 'localhost'
PORT = 8000
s = None

CLIENT_NAME = raw_input('Enter client name: ')

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
        print 'could not open socket'
        sys.exit(1)

    command = raw_input('Enter client command: ')
    #command = "placeholder"
    #recieve = True

    if "JOIN_CHATROOM" in command:
        chatroom = re.sub('JOIN_CHATROOM ', '', command)
        s.sendall('JOIN_CHATROOM: ' + chatroom +'\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: ' + CLIENT_NAME + '\n')
        sys.stdout.write('SEND_MESSAGE '); sys.stdout.flush()
        recieve = True

    if "SEND_MESSAGE" in command:
        if ROOM_REF != '':
            message = re.sub('SEND_MESSAGE ', '', command)
            s.sendall('CHAT: ' + ROOM_REF +'\nJOIN_ID: ' + JOIN_ID + '\nCLIENT_NAME: ' + CLIENT_NAME + '\nMESSAGE: ' + message + '\n')
            recieve = True
        else:
            print 'ROOM_REF not set up.'

    if "HELO" in command:
        s.sendall('HELO text\n')
        recieve = True

    if recieve == True:
     #   while 1:
       #     socket_list = [sys.stdin, s]
        #    # Get the list sockets which are readable
         #   read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
          #  print ("test")
           # for sock in read_sockets: 
            #    if sock == s:
             #       print ("sock found!")
              #      # incoming message from remote server, s
               #     data = sock.recv(4096)
                #    if not data :
                 #       print '\nDisconnected from chat server'
                  #      sys.exit()
                   # else :
                    #    #print data
                     #   sys.stdout.write(data)
                      #  sys.stdout.write('SEND_MESSAGE '); sys.stdout.flush()     
                #
                #else :
                 #   # user entered a message
                  #  msg = sys.stdin.readline()
                   # s.send(msg)
                    #sys.stdout.write('SEND_MESSAGE '); sys.stdout.flush() 

        data = s.recv(1024)

        if "JOINED_CHATROOM:" in data:
            joined_lines = data.split('\n')
            CHATROOM_NAME = re.sub('JOINED_CHATROOM: ', '', joined_lines[0])
            SERVER_IP = re.sub('SERVER_IP: ', '', joined_lines[1])
            SERVER_PORT = re.sub('PORT: ', '', joined_lines[2])
            ROOM_REF = re.sub('ROOM_REF: ', '', joined_lines[3])
            JOIN_ID = re.sub('JOIN_ID: ', '', joined_lines[4])
            print('Joined chatroom...')

        if "CHAT:" in data:
            chat_lines = data.split('\n')
            sender = re.sub('CLIENT_NAME: ', '', chat_lines[1])
            chat_message = re.sub('MESSAGE: ', '', chat_lines[2])
            print sender + ': ' + chat_message

        s.close()
        print(data)
    else:
        s.close()
