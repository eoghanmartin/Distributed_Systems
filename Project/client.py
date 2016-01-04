# echo_client.py
#import socket

if __name__ == "__main__":
    from ClientProxy import Proxy

    myProxyObject = Proxy()

    '''data = myProxyObject.create('file2.txt', 2000, 'localhost')
    print('Received', repr(data))

    data = myProxyObject.create('file3.txt', 2000, 'localhost')
    print('Received', repr(data))'''

    #data = myProxyObject.open('file2.txt', 2000, 'localhost')
    #print('Received', repr(data))

    #data = myProxyObject.write('file2.txt', 2000, 'localhost', "testeroony")
    #print('Write', repr(data))

    data = myProxyObject.open('file2.txt', 2000, 'localhost')
    print('Open', repr(data))

    #data = myProxyObject.delete('file2.txt', 2000, 'localhost')
    #print('Delete', repr(data))


