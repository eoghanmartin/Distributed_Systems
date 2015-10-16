if __name__ == '__main__':
    import random
    import time
    import socket
    import sys
    execfile("threadpool.py")

    exit = 0

    def use_client(data):
        global exit
        while 1:
            time.sleep(1)
            client, address = s.accept()
            data = client.recv(size)
            if data == "KILL_SERVICE\n":
                print "closing..."
                exit = 1
            if data == "HELO text\n":
                client.send("HELO text\nIP: " + str(address) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
            print("Result from request: %s" % (data))
            client.close()

    def terminate(data):
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()

    studentID = '677cfc77e52778a3d5741cb5d5f358c537c28f5134d63e4b7f8376f73315922c'
    host = '' 
    port = int(sys.argv[1])
    backlog = 5 
    size = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog)
    sock = [s]

    i = 0

    while True:

        if exit == 1:
            requests = makeRequests(terminate, sock)
            sys.exit()

        else:
            requests = makeRequests(use_client, sock)
            main = ThreadPool(5)
            for req in requests:
                main.putRequest(req)
                print("Work request #%s added." % req.requestID)
            time.sleep(0.5)
            main.poll()
            if i < 10:
                print("Adding a worker thread...")
                main.createWorkers(1)
                i += 1
        s.close

    if main.dismissedWorkers:
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()
