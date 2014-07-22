#!/usr/bin/python
#coding=utf-8

import socket
import thread
import time

HOST = '192.168.150.23'
PORT = 8000
content = {}

#Read index.html, put into HTTP response data

def header(type):  # text/html   image/jpg
    return '''
HTTP/1.x 200 ok
Content-Type: ''' + type + '''

'''

def importer(filename, key):
    file = open(filename, 'rb')
    head = header(key+'/'+filename.split('.')[-1]) # expanded name
    try:
        content[key][filename] = head + file.read()
    except KeyError:
        file.seek(0)
        content[key] = {filename:(head + file.read())}
    file.close()


def tracer(src):
    src = filter(lambda x:x, src.split('/'))
    con = content
    print src
    for num,item in enumerate(src):
        try:
            con = con[item]
        except KeyError:
            return content["text"]["404.html"]
    if type(con) != str:
        return content["text"]["404.html"]
    return con


def serve(client, addr):
    thtime = time.ctime()
    print "\n\nNew thread started at",thtime
    request = client.recv(5192)
    method = request.split(' ')[0]
    src = request.split(' ')[1]

    print "===== info ====="
    print "Client connected\t:\t",addr
    print "==== Request ===\r\n" ,request

    if method == 'GET':
        ret = tracer(src)  #corresponding file            

    client.sendall(ret)
    client.close()
    print "Thread of",thtime,"finished\n\n"


filter(lambda (x,y):importer(x,y),[
    ( "index.html"   ,   "text"  ),
    ( "reg.html"     ,   "text"  ),
    ( "scenary.jpg"  ,   "image" ),
    ( "404.html"     ,   "text"  ),
])



if __name__ == "__main__":
    try:
        #Socket Init
        server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(500)
        server.bind((HOST,PORT))
        server.listen(100)
        while True:
            client, addr = server.accept()
            thread.start_new_thread(serve, (client, addr))

    except (KeyboardInterrupt, SystemExit):
        pass

    server.close()
