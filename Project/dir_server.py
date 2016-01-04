#! /usr/bin/env python
import SocketServer, subprocess, sys, pdb
from threading import Thread
import socket

HOST = 'localhost'
PORT = 2000


HASHED_FILE_ADDRESSES = []
HASHED_FILE_PORTS = []
HASHED_FILE_FILES = []
HASHED_FILE_LOCKS = []
WRITE_PORT = ''
WRITE_ADDRESS = ''

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global WRITE_ADDRESS
        global WRITE_PORT
        data = self.request.recv(1024)
        commands = data.split('\n')
        if data:
            print ('\n\nDATA IN:' + data)
        ## OPEN ##
        if "OPEN_" in data:
            print('SEARCHING FOR FILE...\n')
            print (HASHED_FILE_FILES)
            hashedFileName = str(hash(commands[1]))
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                returnData = hashedFileName + '\n' + file_host + '\n' + file_port
                print ('FOUND: ' + returnData)
                self.request.send(returnData)
            else:
                print('ERROR: Could not find file.\n')
                self.request.send("ERROR: Could not find file.\n")
        ## CREATE ##
        elif "CREATE_" in data:
            print('SEARCHING FOR SERVER...\n')
            print (HASHED_FILE_LOCKS)
            hashedFileName = str(hash(commands[1]))
            file_host = 'localhost'
            file_port = '8888'
            returnData = hashedFileName + '\n' + file_host + '\n' + file_port
            print returnData
            newFileCreated(hashedFileName, file_host, file_port, 'FileDetails.txt')
            self.request.send(returnData)
        ## DELETE ##
        elif "DELETE_" in data:
            print('SEARCHING FOR SERVER...\n')
            hashedFileName = str(hash(commands[1]))
            lock_set = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                lock_set = self.setLock(file_port, file_host)
                if lock_set == True:
                    returnData = hashedFileName + '\n' + file_host + '\n' + file_port
                    print ('DELETING: ' + returnData)
                    print (HASHED_FILE_LOCKS)
                    print (HASHED_FILE_FILES)
                    self.request.send(returnData)
                else:
                    print('ERROR: (Delete) Problem with locking file.\n')
                    self.request.send("ERROR: (Delete) Problem with locking file.\n")
            else:
                print('ERROR: (Delete) Could not find file.\n')
                self.request.send("ERROR: (Delete) Could not find file.\n")
        ## DELETE UNLOCK ##
        elif "DELETED_" in data:
            print('SEARCHING FOR SERVER...\n')
            hashedFileName = str(hash(commands[1]))
            lock_clear = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                lock_clear = self.clearLock(file_port, file_host)
                if lock_clear == True:
                    returnData = 'OK\n'
                    print ('DELETING: ' + returnData)
                    print (HASHED_FILE_LOCKS)
                    print (HASHED_FILE_FILES)
                    self.request.send(returnData)
                else:
                    print('ERROR: (Delete) Problem with locking file.\n')
                    self.request.send("ERROR: (Delete) Problem with locking file.\n")
            else:
                print('ERROR: (Delete) Could not find file.\n')
                self.request.send("ERROR: (Delete) Could not find file.\n")
        ## WRITE ##
        elif "WRITE_" in data:
            print('SEARCHING FOR FILE...\n')
            hashedFileName = str(hash(commands[1]))
            lock_set = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                lock_set = self.setLock(file_port, file_host)
                if lock_set == True:
                    returnData = hashedFileName + '\n' + file_host + '\n' + file_port
                    print ('FOUND AND LOCKED FILE: ' + returnData)
                    self.request.send(returnData)
                else:
                    print('ERROR: (Write) Problem with locking file.\n')
                    self.request.send("ERROR: Problem with locking file.\n")
            else:
                print('ERROR: (Write) Could not find file.\n')
                self.request.send("ERROR: (Write) Could not find file.\n")
        ## WRITE UNLOCK ##
        elif "WRITTEN_" in data:
            print('SEARCHING FOR FILE...\n')
            hashedFileName = str(hash(commands[1]))
            lock_clear = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                lock_clear = self.clearLock(file_port, file_host)
                if lock_clear == True:
                    returnData = hashedFileName + '\n' + file_host + '\n' + file_port
                    print ('FOUND AND UNLOCKED FILE: ' + returnData)
                    self.request.send(returnData)
                else:
                    print('ERROR: (Written) Problem with unlocking file.\n')
                    self.request.send("ERROR: (Written) Problem with unlocking file.\n")
            else:
                print('ERROR: (Written) Could not find file to unlock.\n')
                self.request.send("ERROR: (Written) Could not find file to unlock.\n")
        else:
            print('COMMAND NOT RECOGNISED\n')
            self.request.send('ERROR: Command not recognised.\n')
        self.request.close()

    def getPort(self, hashedFileName):
        file_port = ''
        i = 0
        if hashedFileName in HASHED_FILE_FILES:
            for a in HASHED_FILE_FILES:
                if a == hashedFileName:
                    file_port = HASHED_FILE_PORTS[i]
                    return file_port
                i = i + 1
        return ''

    def getAddress(self, hashedFileName):
        file_host = ''
        i = 0
        if hashedFileName in HASHED_FILE_FILES:
                for a in HASHED_FILE_FILES:
                    if a == hashedFileName:
                        file_host = HASHED_FILE_ADDRESSES[i]
                        return file_host
                    i = i + 1
        return ''

    def setLock(self, port, host):
        y = 0
        for a in HASHED_FILE_ADDRESSES:
            if a == host:
                p = HASHED_FILE_PORTS[y]
                if p == port:
                    if HASHED_FILE_LOCKS[y] == 0:
                        HASHED_FILE_LOCKS[y] = 1
                        return True
            y=y+1
        return False

    def clearLock(self, port, host):
        y = 0
        for a in HASHED_FILE_ADDRESSES:
            if a == host:
                p = HASHED_FILE_PORTS[y]
                if p == port:
                    if HASHED_FILE_LOCKS[y] == 1:
                        HASHED_FILE_LOCKS[y] = 0
                        return True
            y=y+1
        return False

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def newFileCreated(newFileName, newFileHost, newFilePort, fileDetailsFile):
    with open(fileDetailsFile) as f:
        file_details = f.readlines()
    f.close()
    if file_details:
        with open(fileDetailsFile, "a") as fileDetails:
            fileDetails.write("\n" + newFileName + "   '" + newFileHost + "' " + newFilePort)
    else:
        with open(fileDetailsFile, "a") as fileDetails:
            fileDetails.write(newFileName + "   '" + newFileHost + "' " + newFilePort)
    fileDetails.close()
    HASHED_FILE_LOCKS.append(0)
    setupFilesList(fileDetailsFile)

def setupFilesList(fileDetailsFile):
    global WRITE_ADDRESS
    global WRITE_PORT
    del HASHED_FILE_ADDRESSES[:]
    del HASHED_FILE_PORTS[:]
    del HASHED_FILE_FILES[:]
    with open(fileDetailsFile) as f:
        file_details = f.readlines()
    f.close()
    i = 0
    if file_details:
        for f in file_details:
            details = f.split()
            HASHED_FILE_ADDRESSES.append(details[1].replace("'",""))
            HASHED_FILE_PORTS.append(details[2].replace("'",""))
            HASHED_FILE_FILES.append(details[0].replace("'",""))
            WRITE_ADDRESS = details[1].replace("'","")
            WRITE_PORT = details[2].replace("'","")
            

def setupLocks():
    global HASHED_FILE_LOCKS
    i = 0
    for a in HASHED_FILE_ADDRESSES:
        HASHED_FILE_LOCKS.append(0)
        i=i+1

if __name__ == "__main__":

    setupFilesList('FileDetails.txt')
    setupLocks()
    print (HASHED_FILE_LOCKS)
    server = SimpleServer((HOST, PORT), SingleTCPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exikt(0)
