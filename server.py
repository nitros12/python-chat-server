import socket, threading
def broadcast(message, sender): #sends data, taken from a website, but so simple, not really any issue
    for socket in connections:
        if socket != server and socket != sender:
            try:
                socket.send(message)
            except: #cannot send, drop client
                print('{} dropped'.format(socket))
                #socket.close()
                #connections.remove(socket)

connections = []
buffer = 4096
port = 50001
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", port))
server.listen(10)
# generates the server tcp listener and broadcaster
connections.append(server) #adds server to sockets
def handle_connect():
    while True:
        print('waiting')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 5000))
        s.listen(1)
        conn, addr = s.accept() #wait for a connection
        connections[addr] = conn #add connection to connections
        broadcast('client connected on: {}'.format(addr),server) #tell all users that message has been sent
        print('client connected on: {}'.format(addr),server)
        threading.Thread(target=handle_recv(conn)).start()
        print('test')
    
def handle_recv(conn):
    print('user handled')
    while True:
        print('tick')
        try:
            data = conn.recv(buffer)
            print(data)
            if data:
                broadcast(data, conn)
        except:
            print('{} disconnected'.format(conn))
            conn.close()
            connections.remove(conn)
            break
threading.Thread(target=handle_connect).start()

