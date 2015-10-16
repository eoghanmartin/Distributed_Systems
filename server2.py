if __name__ == '__main__':
    import random
    import time
    import socket
    import sys
    execfile("threadpool.py")

    def do_something(data):
        while 1:
            time.sleep(1)
            client, address = s.accept()
            data = client.recv(size) 
            if data == "HELO text\n":
                client.send("HELO text\nIP:[ip address]\nPort:[port number]\nStudentID:[your student ID]\n")
            print("**** Result from request #%s: " % (data))
            client.close()

    def handle_exception(request, exc_info):
        if not isinstance(exc_info, tuple):
            print(request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % \
          (request.requestID, exc_info))

    host = '' 
    port = 8000 
    backlog = 5 
    size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog)

    socket = [s]

    requests = makeRequests(do_something, socket, handle_exception)

    print("Creating thread pool with 2 worker threads.")
    main = ThreadPool(5)

    for req in requests:
        main.putRequest(req)
        print("Work request #%s added." % req.requestID)

    i = 0
    while True:
        try:
            time.sleep(0.5)
            main.poll()
            print("Main thread working...")
            print("(active worker threads: %i)" % (threading.activeCount()-1, ))
            if i == 20:
                print("**** Dismissing 2 worker threads...")
                main.dismissWorkers(2)
            i += 1
        except KeyboardInterrupt:
            print("**** Interrupted!")
            break
        except NoResultsPending:
            print("**** No pending results.")
            break
    if main.dismissedWorkers:
        print("Joining all dismissed worker threads...")
        main.joinAllDismissedWorkers()