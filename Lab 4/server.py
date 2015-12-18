import threading
from threadpool import makeRequests, ThreadPool
import time
import socket
import sys
import re

exit = 0

if __name__ == '__main__':

    def use_client(data):
        global exit

        CHATROOM_NAME = ''
        SERVER_IP = socket.gethostbyname(socket.gethostname()) 
        SERVER_PORT = str(port)
        ROOM_REF = '1'
        JOIN_ID = '1'
        CLIENT_NAME = ''

        print 'tester'

        while 1:
            time.sleep(1)
            client, address = s.accept()
            data = client.recv(size)
            if "KILL_SERVICE" in data:
                print ("closing...")
                exit = 1
            if "HELO" in data:
                print(data + "IP: " + socket.gethostbyname(socket.gethostname()) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
                client.send(data + "IP: " + socket.gethostbyname(socket.gethostname()) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
            if "JOIN_CHATROOM:" in data:
                join_lines = data.split('\n')
                CHATROOM_NAME = re.sub('JOIN_CHATROOM: ', '', join_lines[0])
                CLIENT_NAME = re.sub('CLIENT_NAME: ', '', join_lines[3])
                print CLIENT_NAME
                client.send('JOINED_CHATROOM: ' + CHATROOM_NAME + '\nSERVER_IP: ' + SERVER_IP + '\nPORT: ' + SERVER_PORT + '\nROOM_REF: ' + ROOM_REF + '\nJOIN_ID: ' + JOIN_ID + '\n')
            if "CHAT:" in data:
                if ROOM_REF != '':
                    chat_lines = data.split('\n')
                    message = re.sub('MESSAGE: ', '', chat_lines[3])
                    client.send('CHAT: ' + ROOM_REF + '\nCLIENT_NAME: ' + CLIENT_NAME + '\nMESSAGE: ' + message + '\n')
            print(data)
            client.close()

    def update_client(data):
        CHATROOM_NAME = ''
        ROOM_REF = '1'
        JOIN_ID = '1'
        CLIENT_NAME = ''

        connected = False

        while connected == False:
            client, address = s.accept()
            data = client.recv(size)
            if "JOIN_CHATROOM:" in data:
                join_lines = data.split('\n')
                ROOM_REF = re.sub('ROOM_REF: ', '', join_lines[0])
                CHATROOM_NAME = re.sub('JOIN_ID: ', '', join_lines[1])
                CLIENT_NAME = re.sub('CLIENT_NAME: ', '', join_lines[2])
                connected = True
            client.close()

        while 1:
            time.sleep(1)
            new_message = False
            #check file for new message...
            new_message = True
            if new_message == True:
                client, address = s.accept()
                client.send('test loop\n')
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
            updates = makeRequests(update_client, sock)
            for update in updates:
                main.putRequest(update)
            time.sleep(0.5)
            main.poll()
        s.close
    if main.dismissedWorkers:
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()