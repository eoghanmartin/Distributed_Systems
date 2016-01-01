import threading
from threadpool import makeRequests, ThreadPool
import time
import socket
import sys
import re
import pdb

exit = 0

CHATROOM_NAME = ''
SERVER_IP = socket.gethostbyname(socket.gethostname()) 
SERVER_PORT = '8000'
ROOM_REF = '1'
JOIN_ID = '1'
CLIENT_NAME = ''

if __name__ == '__main__':

    def use_client(data):
        global exit
        while 1:
            time.sleep(1)
            client, address = s.accept()
            data = client.recv(size)
            data = str(data,"UTF-8")
            if data:
                print ('DATA IN:' + data)
            if "KILL_SERVICE" in data:
                print ("closing...")
                exit = 1
            if "HELO" in data:
                print('HELO RELAY\n')
                sendData = bytes(data,"UTF-8")
                client.send(sendData)
            if "JOIN_CHATROOM:" in data:
                join_lines = data.split('\n')
                CHATROOM_NAME = join_lines[0].split(':')[1]
                CLIENT_NAME = join_lines[3].split(':')[1]
                print('---PARSED INFO---\n' + 'CHATROOM_NAME: ' + CHATROOM_NAME + '\nCLIENT_NAME: ' + CLIENT_NAME + '\n')
                joinString = 'JOINED_CHATROOM: ' + CHATROOM_NAME + '\nSERVER_IP: ' + SERVER_IP + '\nPORT: ' + SERVER_PORT + '\nROOM_REF: ' + ROOM_REF + '\nJOIN_ID: ' + JOIN_ID + '\n'
                sendData = bytes(joinString,"UTF-8")
                client.send(sendData)
            if "CHAT:" in data:
                if ROOM_REF != '':
                    chat_lines = data.split('\n')
                    message = re.sub('MESSAGE: ', '', chat_lines[3])
                    client.send('CHAT: ' + ROOM_REF + '\nCLIENT_NAME: ' + CLIENT_NAME + '\nMESSAGE: ' + message + '\n')
            client.close()

    studentID = '677cfc77e52778a3d5741cb5d5f358c537c28f5134d63e4b7f8376f73315922c'
    host = ''
    port = int(sys.argv[1])
    backlog = 5
    size = 1024
    threads = 5

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog)
    sock = [s]

    main = ThreadPool(threads)
    main.createWorkers(threads)

    while True:

        if exit == 1:
            sys.exit()

        else:
            requests = makeRequests(use_client, sock)
            for req in requests:
                main.putRequest(req)
            time.sleep(0.5)
            main.poll()
        s.close
    if main.dismissedWorkers:
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()
