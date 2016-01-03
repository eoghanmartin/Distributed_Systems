# echo_client.py
#import socket

if __name__ == "__main__":
    from ClientProxy import Proxy

    myProxyObject = Proxy()

    data = myProxyObject.delete('file5.txt', 2000, 'localhost')
    print('Received', repr(data))

    data = myProxyObject.open('file1.txt', 2000, 'localhost')
    print('Received', repr(data))

    #data = myProxyObject.create('file5.txt', 2000, 'localhost')
    #print('Create', repr(data))

    #data = myProxyObject.write('file3.txt', 'new text\n', 2000, 'localhost')
    #print('Write', repr(data))


