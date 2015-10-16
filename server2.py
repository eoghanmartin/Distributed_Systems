if __name__ == '__main__':
    import random
    import time
    import socket
    import sys
    execfile("threadpool.py")

    def use_client(data):
        while 1:
            time.sleep(1)
            client, address = s.accept()
            data = client.recv(size)
            if data == "HELO text\n":
                client.send("HELO text\nIP: " + str(address) + "\nPort: " + str(port) + "\nStudentID: " + studentID + "\n")
            print("Result from request: %s" % (data))
            client.close()

    studentID = '677cfc77e52778a3d5741cb5d5f358c537c28f5134d63e4b7f8376f73315922c'
    host = '' 
    port = 8000 
    backlog = 5 
    size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog)
    socket = [s]

    requests = makeRequests(use_client, socket)

    main = ThreadPool(5)

    for req in requests:
        main.putRequest(req)
        print("Work request #%s added." % req.requestID)

    i = 0
    while True:
        time.sleep(0.5)
        main.poll()
        if i < 10:
            print("Adding a worker thread...")
            main.createWorkers(1)
            i += 1
        #if i == 10:
         #   print("Dismissing 2 worker threads...")
          #  main.dismissWorkers(2)

    if main.dismissedWorkers:
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()