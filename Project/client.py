# echo_client.py
#import socket

if __name__ == "__main__":
    from ClientProxy import Proxy

    myProxyObject = Proxy()

    #data = myProxyObject.create('file1.txt', 2000, 'localhost')
    #print('Received', repr(data))

    #data = myProxyObject.open('file.txt', 2000, 'localhost')
    #print('Received', repr(data))

    #data = myProxyObject.write('file1.txt', 2000, 'localhost', "testeroony")
    #print('Write', repr(data))

    data = myProxyObject.open('file1.txt', 2000, 'localhost')
    print('Open', repr(data))

    #data = myProxyObject.delete('file1.txt', 2000, 'localhost')
    #print('Delete', repr(data))


