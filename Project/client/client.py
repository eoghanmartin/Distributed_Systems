
if __name__ == "__main__":
    from ClientProxy import Proxy

    myProxyObject = Proxy()

    #data = myProxyObject.create('file3.txt')
    #print('Received ' + data)

    #data = myProxyObject.create('file4.txt')
    #print('Received', repr(data))

    #data = myProxyObject.open('file2.txt')
    #print('Received', repr(data))

    #data = myProxyObject.write('file3.txt', "clean")
    #print('Write', repr(data))

    data = myProxyObject.open('file3.txt')
    print('Open', repr(data))

    #data = myProxyObject.delete('file3.txt')
    #print('Delete', repr(data))
