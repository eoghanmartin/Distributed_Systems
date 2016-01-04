#! /usr/bin/env python
import SocketServer, subprocess, sys
from threading import Thread
import socket, os
from FileNames import Files

HOST = 'localhost'
PORT = 8888

filesList = Files()

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        commands = data.split('\n')
        print ('\n\nDATA IN:' + data)
        ## OPEN ##
        if "OPEN_" in data:
            fileNameString = commands[1].replace("'", "")
            print('SEARCHING FOR FILE: ' + fileNameString + '\n')
            if filesList.checkForFile(fileNameString):
                print ('Found file in server.')
                fileIn = open(commands[1] + '.txt', 'r')
                found = fileIn.read()
                fileIn.close()
                print ("FILE CONTENTS: " + found)
                if found:
                    self.request.send(found)
                else:
                    found = '[contents of file empty]'
                    self.request.send(found)
            else:
                print ("ERROR: File not found.\n")
                self.request.send("ERROR: File not found.\n")
        ## CREATE ##
        elif "CREATE_" in data:
            fileIn = open(commands[1] + '.txt', 'w')
            fileIn.close()
            filesList.setupFilesList()
            print ("FILE CONTENTS: [new file]")
            self.request.send('OK')
        ## WRITE ##
        elif "WRITE" in data:
            fileIn = open(commands[1] + '.txt', 'w')
            fileIn.write(commands[2])
            fileIn.close()
            filesList.setupFilesList()
            print ("WRITE TO FILE: " + commands[1])
            self.request.send('OK')
        ## DELETE ##
        elif "DELETE_" in data:
            os.remove(commands[1] + '.txt')
            print ("FILE DELETED")
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

if __name__ == "__main__":

    filesList.setupFilesList()
    
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
