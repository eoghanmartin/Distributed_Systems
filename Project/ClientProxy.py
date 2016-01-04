import socket, pdb

class Proxy():
    
    def open(self, fileName, port, host):
        self.open_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open_s.connect((host, port))
        print('Connection to dir server made.\n')
        self.open_s.sendall('OPEN_\n' + fileName)
        data = self.open_s.recv(1024)
        self.open_s.close()
        if 'ERROR:' in data:
            print(data)
        else:
            if data:
                fileDetails = data.split('\n')
                dir_file = fileDetails[0].replace("'", "")
                dir_host = fileDetails[1].replace("'", "")
                dir_port = int(fileDetails[2].replace("'", ""))
                requestString = 'OPEN_\n' + dir_file
                file_data = self.__sendToFileServer(requestString, dir_host, dir_port)
                if file_data:
                    print('RETURNING FILE DATA...\n')
                    if 'ERROR:' in file_data:
                        return 'ERROR FOUND-- ' + file_data
                    else:
                        return file_data
                else:
                    print('ERROR: Could not find file.\n')
                    return 'ERROR: Could not find file.\n'
            else:
                return 'ERROR: returned - ' + data

    def create(self, fileName, port, host):
        print('CREATING FILE...\n')
        self.create_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.create_s.connect((host, port))
        print('Connection to dir server made.\n')
        self.create_s.sendall('CREATE_\n' + fileName)
        data = self.create_s.recv(1024)
        self.create_s.close()
        if 'ERROR:' in data:
            print(data)
        else:
            if data:
                print('FILE SERVER FOUND\n')
                print (data)
                fileDetails = data.split('\n')
                dir_file = fileDetails[0].replace("'", "")
                dir_host = fileDetails[1].replace("'", "")
                #pdb.set_trace()
                dir_port = int(fileDetails[2].replace("'", ""))
                requestString = 'CREATE_\n' + dir_file
                file_data = self.__sendToFileServer(requestString, dir_host, dir_port)
                if 'OK' in file_data:
                    print('FILE CREATED.\n')
                    return 'OK'
                else:
                    print('ERROR: Could not create file.\n')
                    return 'ERROR: Could not create file.\n'
            else:
                return 'ERROR: returned - ' + data

    def delete(self, fileName, port, host):
        print('DELETING FILE...\n')
        self.delete_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.delete_s.connect((host, port))
        print('Connection to dir server made.\n')
        self.delete_s.sendall('DELETE_\n' + fileName)
        data = self.delete_s.recv(1024)
        if 'ERROR:' in data:
            print(data)
            return 'ERROR: Could not delete file.\n'
        else:
            if data:
                print('FILE SERVER FOUND\n')
                print (data)
                fileDetails = data.split('\n')
                dir_file = fileDetails[0].replace("'", "")
                dir_host = fileDetails[1].replace("'", "")
                dir_port = int(fileDetails[2].replace("'", ""))
                requestString = 'DELETE_\n' + dir_file
                file_data = self.__sendToFileServer(requestString, dir_host, dir_port)
                if 'OK' in file_data:
                    print('FILE DELETED.\n')
                    print ('CLEANING UP')
                    self.delete_s.sendall('DELETED_\n' + fileName)
                    data = self.delete_s.recv(1024)
                    if 'OK' in data:
                        self.delete_s.close()
                        return 'OK'
                    else:
                        data = self.delete_s.sendall('DELETE_FAIL\n' + fileName)
                        if 'ERROR:' in data:
                            return 'ERROR: Internal server error.'
                        else:
                            return 'OK'
                else:
                    print('ERROR: Could not delete file.\n')
                    return 'ERROR: Could not delete file.\n'
            else:
                return 'ERROR: returned - ' + data

    def write(self, fileName, port, host, content):
        print('WRITING FILE...\n')
        self.write_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.write_s.connect((host, port))
        print('Connection to dir server made.\n')
        self.write_s.sendall('WRITE_\n' + fileName)
        data = self.write_s.recv(1024)
        if 'ERROR:' in data:
            print(data)
            return 'ERROR: Could not find file.\n'
        else:
            if data:
                print('FILE SERVER FOUND\n')
                print (data)
                fileDetails = data.split('\n')
                dir_file = fileDetails[0].replace("'", "")
                dir_host = fileDetails[1].replace("'", "")
                dir_port = int(fileDetails[2].replace("'", ""))
                requestString = 'WRITE_\n' + dir_file + '\n' + content
                file_data = self.__sendToFileServer(requestString, dir_host, dir_port)
                if 'OK' in file_data:
                    print('FILE WRITTEN.\n')
                    print ('CLEANING UP')
                    self.write_s.sendall('WRITTEN_\n' + fileName)
                    data = self.write_s.recv(1024)
                    if 'OK' in data:
                        self.write_s.close()
                        return 'OK'
                    else:
                        '''
                        data = self.delete_s.sendall('WRITE_FAIL\n' + fileName)
                        if 'ERROR:' in data:
                            return 'ERROR: Internal server error.'
                        else:
                            return 'OK'
                        '''
                        return 'ERROR: Internal server error.'
                else:
                    print('ERROR: Could not delete file.\n')
                    return 'ERROR: Could not delete file.\n'
            else:
                return 'ERROR: returned - ' + data

    def __sendToFileServer(self, data, host, port):
        self.fileServer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileServer_s.connect((host, port))
        print ('Connected to file server.\n')
        self.fileServer_s.sendall(data)
        file_data = self.fileServer_s.recv(1024)
        self.fileServer_s.close()
        return file_data
