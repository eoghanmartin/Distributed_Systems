import socket, pdb

class Proxy():

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dir_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open(self, fileName, port, host):
        self.s.connect((host, port))
        print('Connection to dir server made.\n')
        self.s.sendall('OPEN\n' + fileName)
        data = self.s.recv(1024)
        self.s.close()
        if 'ERROR:' in data:
            print(data)
        else:
            print (data)
            file_data = self.fetchDataFromServer(data)
            if file_data:
                print('RETURNING FILE DATA...\n')
                return file_data
            else:
                print('ERROR: Could not find file.\n')
                return 'ERROR: Could not find file.\n'

    def create(self, fileName, port, host):
        print('CREATING FILE...\n')
        self.create_s.connect((host, port))
        print('Connection to dir server made.\n')
        self.create_s.sendall('CREATE\n' + fileName)
        data = self.create_s.recv(1024)
        self.create_s.close()
        if 'ERROR:' in data:
            print(data)
        else:
            print('FILE SERVER FOUND\n')
            print (data)
            file_created = self.createFileOnSever(data)
            if file_created:
                print('FILE CREATED.\n')
                return 'OK'
            else:
                print('ERROR: Could not create file.\n')
                return 'ERROR: Could not create file.\n'

    def fetchDataFromServer(self, data):
        fileDetails = data.split('\n')
        dir_file = fileDetails[0]
        #pdb.set_trace()
        dir_host = fileDetails[1].replace("'", "")
        dir_port = int(fileDetails[2])
        self.dir_s.connect((dir_host, dir_port))
        print ('Connected to file server.\n')
        requestString = 'OPEN\n' + dir_file
        self.dir_s.sendall(requestString)
        file_data = self.dir_s.recv(1024)
        self.dir_s.close()
        return file_data

    def createFileOnSever(self, data):
        fileDetails = data.split('\n')
        dir_file = fileDetails[0]
        #pdb.set_trace()
        dir_host = fileDetails[1].replace("'", "")
        dir_port = int(fileDetails[2])
        self.serv_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_s.connect((dir_host, dir_port))
        print ('Connected to file server.\n')
        requestString = 'CREATE\n' + dir_file
        self.serv_s.sendall(requestString)
        file_data = self.serv_s.recv(1024)
        self.serv_s.close()
        return file_data
