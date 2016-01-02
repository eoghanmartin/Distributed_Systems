#! /usr/bin/env python
import SocketServer, subprocess, sys
from threading import Thread
import socket

HOST = 'localhost'
PORT = 8888

FILES = []

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        data = self.request.recv(1024)
        commands = data.split('\n')
        print ('DATA IN:' + data)
        if "OPEN" in data:
            fileNameString = commands[1].replace("'", "")
            print('SEARCHING FOR FILE: ' + fileNameString + '\n')
            print (str(len(FILES)))
            found = False
            if fileNameString in FILES:
                found = True
                fileIn = open(commands[1] + '.txt', 'r')
                found = fileIn.read()
                fileIn.close()
                print ("FILE CONTENTS: " + found)
                if found:
                    self.request.send(found)
            else:
                print ("ERROR: File not found.\n")
                self.request.send("ERROR: File not found.\n")
        elif "CREATE" in data:
            fileIn = open(commands[1] + '.txt', 'w')
            fileIn.close()
            newFileCreated(commands[1], 'fileNames.txt')
            print ("FILE CONTENTS: [new file]")
            self.request.send('OK')
        else:
            print('COMMAND NOT RECOGNISED\n')
            self.request.send('ERROR: Command not recognised.')
        self.request.close()

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def newFileCreated(newFileName, fileDetailsFile):
    with open(fileDetailsFile, "a") as fileDetails:
        fileDetails.write("\n" + newFileName)
    fileDetails.close()
    setupFilesList(fileDetailsFile)

def setupFilesList(fileDetailsFile):
    with open(fileDetailsFile) as f:
        file_details = f.readlines()
    f.close()

    FILES = file_details

if __name__ == "__main__":

    setupFilesList('fileNames.txt')
    
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
