import socket, threading, sys, random

def placer():
    sys.stdout.write('> ')
    sys.stdout.flush()

def getinfo():
    name = str(input('please enter your username: '))
    ip = str(input('please enter the ip of the server: '))
    return ip, name

def connect(ip, name):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip,5000))
    except:
        print('error: cannot connect!')
        sys.exit()
        return #if run from idle, will return to kill the program
    print('connected to {}'.format(ip))
    while True:
        data = server.recv(4096)
        if not data:
            #assume disconnected
            server.close()
            print('you have been ejected from the server')
        if data != '':
            data = data.decode('UTF-8')
            if '#*#givename#*#' in data.strip():
                server.send(name.encode('UTF-8'))
                print('name sent')
            else:
                sys.stdout.write('\r{}\n'.format(data.strip()))
                prompt()
ip, name = getinfo()
connect(ip, name)
    
