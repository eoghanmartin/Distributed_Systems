#! /usr/bin/env python
import SocketServer, subprocess, sys, pdb
from threading import Thread
import socket

HOST = '127.0.0.1'
PORT = 2000

HASHED_FILE_ADDRESSES = []
HASHED_FILE_PORTS = []
HASHED_FILE_FILES = []
HASHED_FILE_LOCKS = []
HOSTS = []
PORTS = []

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        commands = data.split('\n')
        if data:
            print ('\n\nDATA IN:' + data)
        ##########
        ## OPEN ##
        if "OPEN_" in data:
            print('SEARCHING FOR FILE...\n')
            print (HASHED_FILE_FILES)
            print (HASHED_FILE_LOCKS)
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
        ############
        ## CREATE ##
        elif "CREATE_" in data:
            print('SEARCHING FOR SERVER...\n')
            print (HASHED_FILE_LOCKS)
            hashedFileName = str(hash(commands[1]))
            file_host = HOSTS[0]
            file_port = PORTS[0]
            returnData = hashedFileName + '\n' + file_host + '\n' + str(file_port)
            print returnData
            newFileCreated(hashedFileName, file_host, file_port, 'FileDetails.txt')
            self.request.send(returnData)
        ## REPLICATE CREATED FILE ##
        elif "CREAT_ED" in data:
            print('REPLICATING CREATED FILE...\n')
            hashedFileName = str(commands[1])
            file_host = commands[2]
            file_port = commands[3].replace("'","")
            replicated = replicateFilesOnSystem(file_host, int(file_port), hashedFileName)
            if 'OK' in replicated:
                self.request.send("OK")
            else:
                self.request.send("ERROR: Trouble replicating files.")
        ############
        ## DELETE ##
        elif "DELETE_" in data:
            print('SEARCHING FOR SERVER...\n')
            hashedFileName = str(hash(commands[1]))
            lock_set = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                lock_set = self.setLock(file_port, file_host, hashedFileName)
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
        elif "DELETION_" in data:
            print('SEARCHING FOR SERVER...\n')
            hashedFileName = str(commands[1])
            lock_clear = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                lock_clear = self.clearLock(file_port, file_host, hashedFileName)
                if lock_clear == True:
                    returnData = 'OK\n'
                    print ('DELETING: ' + returnData)
                    print (HASHED_FILE_LOCKS)
                    print (HASHED_FILE_FILES)
                    #removeFileDeleted(hashedFileName, file_port, file_host)
                    self.request.send(returnData)
                else:
                    print('ERROR: (Delete) Problem with locking file.\n')
                    self.request.send("ERROR: (Delete) Problem with locking file.\n")
            else:
                print('ERROR: (Delete) Could not find file.\n')
                self.request.send("ERROR: (Delete) Could not find file.\n")
        ###########
        ## WRITE ##
        elif "WRITE_" in data:
            print('SEARCHING FOR FILE...\n')
            hashedFileName = str(hash(commands[1]))
            lock_set = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            if file_port != '' and file_host != '':
                lock_set = self.setLock(file_port, file_host, hashedFileName)
                if lock_set == True:
                    returnData = hashedFileName + '\n' + file_host + '\n' + file_port
                    print ('FOUND AND LOCKED FILE: ' + returnData)
                    print (HASHED_FILE_LOCKS)
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
            hashedFileName = str(commands[1])
            lock_clear = False
            file_port = self.getPort(hashedFileName)
            file_host = self.getAddress(hashedFileName)
            print ('HOST AND PORT: ' + file_host + ' ' + file_port)
            if file_port != '' and file_host != '':
                lock_clear = self.clearLock(file_port, file_host, hashedFileName)
                if lock_clear == True:
                    returnData = hashedFileName + '\n' + file_host + '\n' + file_port
                    print ('FOUND AND UNLOCKED FILE: ' + returnData)
                    replicated = replicateFilesOnSystem(file_host, int(file_port), hashedFileName)
                    self.request.send('OK')
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

    ###############

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

    def setLock(self, port, host, name):
        y = 0
        for a in HASHED_FILE_ADDRESSES:
            if a == host:
                p = HASHED_FILE_PORTS[y]
                if p == port:
                    f = HASHED_FILE_FILES[y]
                    if f == name:
                        if HASHED_FILE_LOCKS[y] == 0:
                            HASHED_FILE_LOCKS[y] = 1
                            return True
            y=y+1
        return False

    def clearLock(self, port, host, name):
        y = 0
        for a in HASHED_FILE_ADDRESSES:
            if a == host:
                p = HASHED_FILE_PORTS[y]
                if p == port:
                    f = HASHED_FILE_FILES[y]
                    if f == name:
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
    if file_details and 'ERROR:' not in newFileName:
        with open(fileDetailsFile, "a") as fileDetails:
            fileDetails.write("\n" + newFileName + "   '" + newFileHost + "' " + str(newFilePort))
    else:
        with open(fileDetailsFile, "a") as fileDetails:
            fileDetails.write(newFileName + "   '" + newFileHost + "' " + newFilePort)
    fileDetails.close()
    HASHED_FILE_LOCKS.append(0)
    updateFilesList(fileDetailsFile)

def replicateFilesOnSystem(fileHost, filePort, fileName):
    rep_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i = 0
    for server in PORTS:
        host = HOSTS[i]
        port = PORTS[i]
        if port != filePort:
            rep_s.connect((host, port))
            print ('Connected to file server.\n')
            rep_data = 'REPLICATE_' + '\n' + host + '\n' + str(port) + '\n' + fileName
            rep_s.sendall(rep_data)
            rep_s.close()
        i = i + 1
    return 'OK'

def removeFileDeleted(hashedFileName, file_port, file_host):
    with open('FileDetails.txt') as fileIn:
        file_details = fileIn.readlines()
    for f in file_details:
        if hashedFileName in f:
            file_details.remove(f)
    fileIn.close()
    fileInAgain = open('FileDetails.txt', 'w')
    fileInAgain.truncate()
    for f in file_details:
        fileInAgain.write(f)
    fileInAgain.close()
    updateFilesList('FileDetails.txt')

def updateFilesList(fileDetailsFile):
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
            

def setupFilesList(fileDetailsFile, fileServersFile):
    global HOSTS
    global PORTS
    del HOSTS[:]
    del PORTS[:]
    clearFileDetails(fileDetailsFile)
    with open(fileServersFile) as s:
        file_servers = s.readlines()
    s.close()
    for servers in file_servers:
        details = servers.split()
        host = details[0].replace("'", "")
        port = int(details[1].replace("'", ""))
        PORTS.append(port)
        HOSTS.append(host)
        data = host + '\n' + str(port)
        filesFromServer = sendToFileServer(data)
        if filesFromServer:
            files = filesFromServer.split('\n')
            for f in files:
                if 'ERROR:' not in f:
                    newFileCreated(f, details[0], details[1], fileDetailsFile)
        else:
            print ('No files on server with port ' + str(port) + ' and add ress ' + host + '.')

def clearFileDetails(fileDetailsFile):
    fileInAgain = open(fileDetailsFile, 'w')
    fileInAgain.write('')
    fileInAgain.close()

def sendToFileServer(data):
        fileServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = data.split('\n')
        host = address[0].replace("'", "")
        port = int(address[1].replace("'", ""))
        fileServer_s.connect((host, port))
        print ('Connected to file server.\n')
        data = 'FILES_'
        fileServer_s.sendall(data)
        file_data = fileServer_s.recv(1024)
        fileServer_s.close()
        return file_data

if __name__ == "__main__":

    setupFilesList('FileDetails.txt', 'FileServers.txt')
    print (HASHED_FILE_FILES)
    print (HASHED_FILE_ADDRESSES)
    server = SimpleServer((HOST, PORT), SingleTCPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
