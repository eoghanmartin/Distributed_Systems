import socket, pdb

dirPort = 2000
dirHost = '127.0.0.1'

class Proxy():
    
    def open(self, fileName):
        self.open_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open_s.connect((dirHost, dirPort))
        print('Connection to dir server made.\n')
        self.open_s.sendall('OPEN_\n' + fileName)
        data = self.open_s.recv(1024)
        self.open_s.close()
        if 'ERROR:' in data:
            return data
        else:
            if data:
                fileDetails = data.split('\n')
                opening_file = fileDetails[0].replace("'", "")
                fileServer_host = fileDetails[1].replace("'", "")
                fileServer_port = int(fileDetails[2].replace("'", ""))
                requestString = 'OPEN_\n' + opening_file
                file_data = self.__sendToFileServer(requestString, fileServer_host, fileServer_port)
                if file_data:
                    print('RETURNING FILE DATA...\n')
                    return file_data
                else:
                    return 'ERROR: Could not find file.\n'
            else:
                return data

    def create(self, fileName):
        print('CREATING FILE...\n')
        self.create_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_s.connect((dirHost, dirPort))
        print('Connection to dir server made.\n')
        self.create_s.sendall('CREATE_\n' + fileName)
        data = self.create_s.recv(1024)
        self.create_s.close()
        if 'ERROR:' in data:
            return data
        else:
            if data:
                print('FILE SERVER FOUND\n')
                fileDetails = data.split('\n')
                new_file = fileDetails[0].replace("'", "")
                fileServer_host = fileDetails[1].replace("'", "")
                fileServer_port = int(fileDetails[2].replace("'", ""))
                requestString = 'CREATE_\n' + new_file
                file_data = self.__sendToFileServer(requestString, fileServer_host, fileServer_port)
                if 'OK' in file_data:
                    print('FILE SERVER FOUND\n')
                    requestString = 'CREAT_ED\n' + new_file + '\n' + fileServer_host + '\n' + str(fileServer_port)
                    replicated = self.__sendToFileServer(requestString, dirHost, dirPort)
                    #pdb.set_trace()
                    if 'OK' in replicated:
                        return 'OK'
                    else:
                        return replicated
                else:
                    return file_data
            else:
                return data

    def delete(self, fileName):
        print('DELETING FILE...\n')
        self.delete_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.delete_s.connect((dirHost, dirPort))
        print('Connection to dir server made.\n')
        self.delete_s.sendall('DELETE_\n' + fileName)
        data = self.delete_s.recv(1024)
        self.delete_s.close()
        if 'ERROR:' in data:
            return data
        else:
            if data:
                print('FILE SERVER FOUND\n')
                fileDetails = data.split('\n')
                dir_file = fileDetails[0].replace("'", "")
                dir_host = fileDetails[1].replace("'", "")
                dir_port = int(fileDetails[2].replace("'", ""))
                requestString = 'DELETE_\n' + dir_file
                file_data = self.__sendToFileServer(requestString, dir_host, dir_port)
                if 'OK' in file_data:
                    return 'OK'
                else:
                    return file_data
            else:
                return data

    def write(self, fileName, content):
        print('WRITING FILE...\n')
        self.write_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.write_s.connect((dirHost, dirPort))
        print('Connection to dir server made.\n')
        self.write_s.sendall('WRITE_\n' + fileName)
        data = self.write_s.recv(1024)
        self.write_s.close()
        if 'ERROR:' in data:
            return data
        else:
            if data:
                print('FILE SERVER FOUND\n')
                fileDetails = data.split('\n')
                dir_file = fileDetails[0].replace("'", "")
                dir_host = fileDetails[1].replace("'", "")
                dir_port = int(fileDetails[2].replace("'", ""))
                requestString = 'WRITE_\n' + dir_file + '\n' + content
                file_data = self.__sendToFileServer(requestString, dir_host, dir_port)

                if 'OK' in file_data:
                    return 'OK'
                else:
                    return file_data
            else:
                return data

    def __sendToFileServer(self, data, host, port):
        self.fileServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileServer_s.connect((host, port))
        print ('Connected to file server.\n')
        self.fileServer_s.sendall(data)
        file_data = self.fileServer_s.recv(1024)
        self.fileServer_s.close()
        return file_data
