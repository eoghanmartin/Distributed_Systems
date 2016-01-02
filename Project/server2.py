#! /usr/bin/env python
import SocketServer, subprocess, sys
from threading import Thread
import socket

HOST = 'localhost'
PORT = 2000

FilesList = []

HASHED_FILE_ADDRESSES = {'fileName': 'address'}
HASHED_FILE_PORTS = {'fileName': 'port'}
LAST_WRITE_ADDRESS = ''
LAST_WRITE_PORT = 0

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        commands = data.split('\n')
        if data:
            print ('DATA IN:' + data)
        if "OPEN" in data:
            print('SEARCHING FOR FILE...\n')
            hashedFileName = str(hash(commands[1]))
            if HASHED_FILE_ADDRESSES[hashedFileName]:
                file_host = HASHED_FILE_ADDRESSES[hashedFileName]
                file_port = HASHED_FILE_PORTS[hashedFileName]
                returnData = hashedFileName + '\n' + file_host + '\n' + file_port
                print ('FOUND: ' + returnData)
                self.request.send(returnData)
            else:
                print('ERROR: Could not find file.\n')
                self.request.send("ERROR: Could not find file.\n")
        if "CREATE" in data:
            print('SEARCHING FOR SERVER...\n')
            hashedFileName = str(hash(commands[1]))
            file_host = 'localhost'
            file_port = 8888
            returnData = hashedFileName + '\n' + file_host + '\n' + str(file_port)
            print returnData
            newFileCreated(hashedFileName, file_host, str(file_port), 'fileDetails.txt')
            self.request.send(returnData)
        else:
            print('COMMAND NOT RECOGNISED\n')
            self.request.send('ERROR: Command not recognised.\n')
        self.request.close()

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def newFileCreated(newFileName, newFileHost, newFilePort, fileDetailsFile):
    with open(fileDetailsFile, "a") as fileDetails:
        fileDetails.write("\n" + newFileName + "   '" + newFileHost + "' " + newFilePort)
    fileDetails.close()
    setupFilesList(fileDetailsFile)

def setupFilesList(fileDetailsFile):
    with open(fileDetailsFile) as f:
        file_details = f.readlines()
    f.close()

    for f in file_details:
        details = f.split()
        HASHED_FILE_ADDRESSES[str(details[0])] = details[1]
        HASHED_FILE_PORTS[str(details[0])] = details[2]

if __name__ == "__main__":

    setupFilesList('fileDetails.txt')

    server = SimpleServer((HOST, PORT), SingleTCPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
