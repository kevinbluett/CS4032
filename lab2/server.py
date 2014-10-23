import asyncore, sys, socket
from async.server import *
from threaded.server import *
from helpers import *

def lab2_handler(server, (sock, addr)):
    data = LithiumHelper.recv_all(sock)
    data = data.replace("\r", "")

    if data == "KILL_SERVICE\n":
        if server is not None:
            Thread(target=server.shutdown, args=[False]).start()
    else:
        sock.send("%sIP:%s\nPort:%s\nStudentID:11311101" % (data, socket.gethostbyname(socket.gethostname()), sys.argv[1]))

    # Kill the socket
    sock.close()
    server.count.decr()

def start_server():
    # # Start the server in async mode
    # server = LithiumAsyncServer('localhost', int(sys.argv[1]), lab2_handler)
    # asyncore.loop()

    # Start the server in thread pool mode
    server = LithiumThreadPoolServer('0.0.0.0', int(sys.argv[1]), lab2_handler)
    server.loop()

if __name__ == '__main__':
    start_server()