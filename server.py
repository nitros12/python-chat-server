import socket
def broadcast(message, sender): #sends data, taken from a website, but so simple, not really any issue
    for socket in connections:
        if socket != server and socket != sender:
            try:
                socket.send(message)
            except: #cannot send, drop client
                socket.close()
                connections.remove(socket)

connections = []
