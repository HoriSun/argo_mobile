#!/usr/bin/python
#coding=utf-8

import socket
import thread
import time
import re
import traceback

HOST = '192.168.150.23'
HOST = ''
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



def htmlreader(filename):
    file = open(filename, 'rb')
    cont = file.read()
    file.close()
    return cont

static_path = './static/'

def staticreader(filename):
    file = open(static_path+filename, 'rb')
    cont = file.read()
    file.close()
    return cont


router = [
    (r'/html/(\w*\.\w+)',htmlreader),
    (r'/static/((?:\w*/)*\w*\.\w+)',staticreader)
]


def route(src):
    for pattern,handler in router:
        mat = re.match(pattern,src)
        if mat:
            try:
                ret = handler(*(mat.groups()))
                return ret
            except Exception, e:
                print "[ ERROR ]\t",e,'\n================================'
                print traceback.format_exc(),"\n\n"
                return ""
    return ""

def serve(client, addr):
    thtime = time.ctime()
    print "\n\nNew thread started at",thtime
    request = client.recv(1024)
    method = request.split(' ')[0]
    src = request.split(' ')[1]

    print "===== info ====="
    print "Client connected\t:\t",addr
    print "==== Request ===\r\n" ,request

    if method == 'GET':
        temp = route(src)  #corresponding file            
        if temp:
            ret = temp
        else:
            ret = route("/text/404.html")

    ret = header('html') + ret   

    client.sendall(ret)
    client.close()
    print "thread",thtime,"finished\n\n"



if __name__ == "__main__":

    try:
        #Socket Init
        server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(500)
        server.bind((HOST,PORT))
        server.listen(100)
        while True:
            client,addr = server.accept()
            thread.start_new_thread(serve,(client, addr))

    except (KeyboardInterrupt, SystemExit):
        pass

    server.close()