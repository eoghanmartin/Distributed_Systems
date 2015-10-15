from SocketServer import ThreadingMixIn
from Queue import Queue
import threading, socket
import time


class ThreadPoolMixIn(ThreadingMixIn):
    numThreads = 10
    allow_reuse_address = True

    def serve_forever(self):
        # set up the threadpool
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target = self.process_request_thread)
            t.setDaemon(1) # makes thread a Daemon thread
            t.start()

        # server main loop
        while True:
            self.handle_request()
        self.server_close()

    
    def process_request_thread(self):
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())

    
    def handle_request(self):
        # add requests to the queue for the workers
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        self.requests.put((request, client_address))
        data = request.recv(1024)
        time.sleep(4)
        if data == "HELO text\n":
            request.sendall("HELO text\nIP:[ip address]\nPort:[port number]\nStudentID:[your student ID]\n")
        print threading.current_thread()
        if not data: return
        print data
        print 'data returned'

if __name__ == '__main__':
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer
    
    class ThreadedServer(ThreadPoolMixIn, TCPServer):
        pass

    def echo(HandlerClass = SimpleHTTPRequestHandler,
            ServerClass = ThreadedServer, 
            protocol="HTTP/1.1"):

        port = 8000
        server_address = ('localhost', port)

        HandlerClass.protocol_version = protocol
        conn = ServerClass(server_address, HandlerClass)

        sa = conn.socket.getsockname()
        print "Serving connection on", sa[0], "port", sa[1], "..."
        conn.serve_forever()

    echo()