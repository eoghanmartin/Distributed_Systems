# echo_client.py
#import socket

if __name__ == "__main__":
    from ClientProxy import Proxy

    myProxyObject = Proxy()

    data = myProxyObject.open('file3.txt', 2000, 'localhost')

    print('Received', repr(data))

    #data = myProxyObject.create('file4.txt', 2000, 'localhost')

    #print('Create', repr(data))

    #data = myProxyObject.write('file3.txt', 'new text\n', 2000, 'localhost')

    #print('Write', repr(data))


