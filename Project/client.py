# echo_client.py
#import socket

if __name__ == "__main__":
    from ClientProxy import Proxy

    myProxyObject = Proxy()

    data = myProxyObject.create('file.txt', 2000, 'localhost')
    print('Received', repr(data))

    data = myProxyObject.open('file.txt', 2000, 'localhost')
    print('Received', repr(data))

    data = myProxyObject.write('file.txt', 2000, 'localhost', "here's some text")
    print('Write', repr(data))

    data = myProxyObject.open('file.txt', 2000, 'localhost')
    print('Received', repr(data))

    #data = myProxyObject.write('file3.txt', 'new text\n', 2000, 'localhost')
    #print('Write', repr(data))


