#! /usr/bin/env python
import SocketServer, subprocess, sys, pdb
from threading import Thread
import socket, os
from FileNames import Files

HOST = '127.0.0.1'
PORT = 7777

dirHost = '127.0.0.1'
dirPort = 2000

filesList = Files()

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        commands = data.split('\n')
        print ('\n\nDATA IN:' + data)
        ##########
        ## OPEN ##
        if "OPEN_" in data:
            print ('OPENING')
            fileNameString = commands[1].replace("'", "")
            print('SEARCHING FOR FILE: ' + fileNameString + '\n')
            allFiles = []
            for f in os.listdir("./files"):
                if fileNameString + '.txt' == f:
                    print ('Found file in server.')
                    fileIn = open('./files/' + fileNameString + '.txt', 'r')
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
        ############
        ## CREATE ##
        elif "CREATE_" in data:
            print ('CREATE')
            fileIn = open('./files/' + commands[1] + '.txt', 'w')
            fileIn.close()
            filesList.setupFilesList()
            print ("FILE CONTENTS: [new file]")
            self.request.send('OK')
        ###########
        ## WRITE ##
        elif "WRITE" in data:
            print ('WRITE')
            fileIn = open('./files/' + commands[1] + '.txt', 'w')
            fileIn.write(commands[2])
            fileIn.close()
            filesList.setupFilesList()
            print ("WRITE TO FILE: " + commands[1])
            dir_file = commands[1].replace("'", "")
            print('FILE WRITTEN.\n')
            print ('CLEANING UP')
            unlock = 'WRITTEN_\n' + dir_file
            data = self.__sendToDirServer(unlock)
            if 'OK' in data:
                print ('File unlocked.')
                self.request.send('OK')
            else:
                # TODO: Failed to unlock. Backtrack the write.
                '''
                data = self.__sendToDirServer('WRITE_FAIL\n' + fileName)
                if 'ERROR:' in data:
                    return 'ERROR: Internal server error.'
                else:
                    return 'OK'
                '''
                self.request.send('ERROR: Internal server error.')
        ############
        ## DELETE ##
        elif "DELETE_" in data:
            print ('DELETE_')
            allFiles = []
            print 'tester for text'
            for file in os.listdir("./files"):
                allFiles.append(file)
            if commands[1] + '.txt' in allFiles:
                os.remove('./files/' + commands[1] + '.txt')
                print ("FILE DELETED")
                dir_file = commands[1].replace("'", "")
                print ('CLEANING UP')
                unlock = 'DELETION_\n' + dir_file
                data = self.__sendToDirServer(unlock)
                if 'OK' in data:
                    print ('File unlocked.')
                    self.request.send('OK')
                else:
                    # TODO: Failed to unlock. Backtrack the delete.
                    '''
                    data = self.__sendToDirServer('WRITE_FAIL\n' + fileName)
                    if 'ERROR:' in data:
                        return 'ERROR: Internal server error.'
                    else:
                        return 'OK'
                    '''
                    self.request.send('ERROR: Internal server error.')
            else:
                self.request.send('ERROR: File doesn\'t exist.')
        ###############
        ## REPLICATE ##
        elif "REPLICATE_" in data:
            print ('REPLICATE')
            newFile = open('./files/' + commands[3] + '.txt', 'w')
            filename = commands[3]
            port = int(commands[2])
            host = commands[1]
            fileData = self.__sendToFileServer(host, port, filename)
            if fileData:
                newFile.write(fileData)
            newFile.close()
            print ('Shes replicated')
        ## RETURN REPLICA ##
        elif "RETURN_REP" in data:
            print ('RETURN REPLICATE')
            with open('./files/' + commands[1] + '.txt', 'r') as myfile:
                rep=myfile.read()
            myfile.close()
            self.request.send(rep)
        #####################
        ## SETUP DIRECTORY ##
        elif 'FILES_' in data:
            print ('FILES')
            allFiles = []
            for f in os.listdir("./files"):
                if '.txt' in f:
                    f = f[:-4]
                    allFiles.append(f)
            files = ''
            if allFiles:
                for name in allFiles:
                    if files:
                        files = files + '\n' + name
                    else:
                        files = name
            if files:
                self.request.send(files)
            else:
                self.request.send('ERROR: File doesn\'t exist.')
        else:
            print('COMMAND NOT RECOGNISED\n')
            self.request.send('ERROR: Command not recognised.')
        self.request.close()

    def __sendToDirServer(self, data):
        self.dirServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dirServer_s.connect((dirHost, dirPort))
        print ('Connected to dir server.\n')
        self.dirServer_s.sendall(data)
        file_data = self.dirServer_s.recv(1024)
        self.dirServer_s.close()
        return file_data

    def __sendToFileServer(self, rep_host, rep_port, filename):
        self.fileServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileServer_s.connect((rep_host, rep_port))
        print ('Connected to dir server.\n')
        rep_data = 'RETURN_REP\n' + filename
        self.fileServer_s.sendall(rep_data)
        file_data = self.fileServer_s.recv(1024)
        self.fileServer_s.close()
        return file_data

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
