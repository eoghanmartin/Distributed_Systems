# echo_client.py
#import socket

if __name__ == "__main__":
    from ClientProxy import Proxy

    myProxyObject = Proxy()

    '''data = myProxyObject.create('file2.txt')
    print('Received', repr(data))

    data = myProxyObject.create('file3.txt')
    print('Received', repr(data))'''

    #data = myProxyObject.open('file2.txt')
    #print('Received', repr(data))

    #data = myProxyObject.write('file2.txt', "testeroony")
    #print('Write', repr(data))

    data = myProxyObject.open('file2.txt')
    print('Open', repr(data))

    #data = myProxyObject.delete('file2.txt')
    #print('Delete', repr(data))


