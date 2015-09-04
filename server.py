import socket, threading
def broadcast(message, sender): #sends data, taken from a website, but so simple, not really any issue
    for name, conn in names.items():
        if name != sender:
            try:
                conn.send(message+'\n')
            except:
                pass
names = {}
buffer = 4096
host = ""
port = 50001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(False)
server.bind(("0.0.0.0", port))
server.listen(10)
def connect(conn):
    def threaded():
        while True:
            conn.send('#*#givename#*#'.encode('UTF-8'))
            try:
                print('waiting for name\n')
                name = conn.recv(1024).strip()
            except:
                continue
            name = name.decode('UTF-8')
            print(name)
            if name in names:
                namenumber = 0
                while name in names: #appends a number to the name if it is already in use
                    print(namenumber)
                    namenumber+=1
                    if ('{} {}'.format(name,namenumber)) not in names:
                        name = '{} {}'.format(name,namenumber)
                        conn.setblocking(False)
                        names[name] = conn
                        broadcast('{} has joined the server\n'.format(name),name)
                        break
            else:
                print('name added')
                name = '{}'.format(name)
                conn.setblocking(False)
                names[name] = conn
                broadcast('{} has joined the server\n'.format(name),name)
                print(names.items())
                break
        print('exited connect loop')
    threading.Thread(target=threaded).start()                       
while True:
    try:
        while True:
            try:
                conn, addr = server.accept()
            except socket.error:
                break
            print('connect')
            connect(conn)
        for name,conn in names: #for loop of items in users
            try:
                print('attempting to receive from {}'.format(name))
                message = conn.recv(1024)
            except socket.error:
                continue
            if not message:
                del users[name]
                broadcast('{} has left'.format(name),name)
            else: #got a message
                broadcast('<{}> {}'.format(name,message.strip()))
    except (SystemExit, KeyboardInterrupt):
        print('exit 1')
        break
