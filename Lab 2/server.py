import threading
from threadpool import makeRequests, ThreadPool
import time
import socket
import sys

exit = 0

if __name__ == '__main__':
    #exec(open("threadpool.py").read())

    def use_client(data):
        global exit
        print (threading.current_thread())
        while 1:
            time.sleep(1)
            client, address = s.accept()
            data = client.recv(size)
            if "KILL_SERVICE" in data:
                print ("closing...")
                exit = 1
            if "HELO" in data:
<<<<<<< HEAD
                print(data + "IP: " + socket.gethostbyname(socket.gethostname()) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
                client.send(data + "IP: " + socket.gethostbyname(socket.gethostname()) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
            if "JOIN_CHATROOM" in data:
                client.send("JOINED_CHATROOM: room1\nSERVER_IP: " + socket.gethostbyname(socket.gethostname()) + "\nPORT: 0\nROOM_REF: 1\nJOIN_ID: 1\n")
=======
                #print(data +"IP: " + str(address) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
                client.send(data + "IP:" + socket.gethostbyname(socket.gethostname()) + "\nPort: " + str(port) + "\nStudentID: " + studentID)
>>>>>>> origin/master
            print("Result from request: %s" % (data))
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
