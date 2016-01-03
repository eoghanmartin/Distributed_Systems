import socket, pdb

class Proxy():
    
    def open(self, fileName, port, host):
        self.open_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open_s.connect((host, port))
        print('Connection to dir server made.\n')
        self.open_s.sendall('OPEN\n' + fileName)
        data = self.open_s.recv(1024)
        self.open_s.close()
        if 'ERROR:' in data:
            print(data)
        else:
            print (data)
            file_data = self.__fetchDataFromServer(data)
            if file_data:
                print('RETURNING FILE DATA...\n')
                if 'ERROR:' in file_data:
                    return 'ERROR FOUND-- ' + file_data
                else:
                    return file_data
            else:
                print('ERROR: Could not find file.\n')
                return 'ERROR: Could not find file.\n'

    def create(self, fileName, port, host):
        print('CREATING FILE...\n')
        self.create_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            file_created = self.__createFileOnServer(data)
            if file_created:
                print('FILE CREATED.\n')
                return 'OK'
            else:
                print('ERROR: Could not create file.\n')
                return 'ERROR: Could not create file.\n'

    def delete(self, fileName, port, host):
        print('DELETING FILE...\n')
        self.delete_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.delete_s.connect((host, port))
        print('Connection to dir server made.\n')
        self.delete_s.sendall('DELETE\n' + fileName)
        data = self.delete_s.recv(1024)
        self.delete_s.close()
        if 'ERROR:' in data:
            print(data)
        else:
            print('FILE SERVER FOUND\n')
            print (data)
            file_created = self.__deleteFileOnServer(data)
            if file_created:
                print('FILE DELETED.\n')
                return 'OK'
            else:
                print('ERROR: Could not delete file.\n')
                return 'ERROR: Could not delete file.\n'

    def __fetchDataFromServer(self, data):
        fileDetails = data.split('\n')
        dir_file = fileDetails[0]
        #pdb.set_trace()
        dir_host = fileDetails[1].replace("'", "")
        dir_port = int(fileDetails[2])
        self.fetch_dirServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fetch_dirServer_s.connect((dir_host, dir_port))
        print ('Connected to file server.\n')
        requestString = 'OPEN\n' + dir_file
        self.fetch_dirServer_s.sendall(requestString)
        file_data = self.fetch_dirServer_s.recv(1024)
        self.fetch_dirServer_s.close()
        return file_data

    def __createFileOnServer(self, data):
        fileDetails = data.split('\n')
        dir_file = fileDetails[0]
        #pdb.set_trace()
        dir_host = fileDetails[1].replace("'", "")
        dir_port = int(fileDetails[2])
        self.create_fileServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_fileServer_s.connect((dir_host, dir_port))
        print ('Connected to file server.\n')
        requestString = 'CREATE\n' + dir_file
        self.create_fileServer_s.sendall(requestString)
        file_data = self.create_fileServer_s.recv(1024)
        self.create_fileServer_s.close()
        return file_data

    def __deleteFileOnServer(self, data):
        fileDetails = data.split('\n')
        dir_file = fileDetails[0]
        dir_host = fileDetails[1].replace("'", "")
        dir_port = int(fileDetails[2])
        self.delete_fileServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.delete_fileServer_s.connect((dir_host, dir_port))
        print ('Connected to file server.\n')
        requestString = 'DELETE\n' + dir_file
        self.delete_fileServer_s.sendall(requestString)
        file_data = self.delete_fileServer_s.recv(1024)
        self.delete_fileServer_s.close()
        return file_data
