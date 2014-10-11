import asyncore, sys
from async.server import *
from threaded.server import *
from helpers import *

def lab2_handler(server, (sock, addr)):
    data = LithiumHelper.recv_all(sock)
    data = data.replace("\r", "")

    if data == "HELO text\n":
        sock.send("HELO text\nIP:%s\nPort:%s\nStudentID:11311101" % addr)
    elif data == "KILL_SERVICE\n":
        if server is not None:
            Thread(target=server.shutdown, args=[False]).start()
    else:
        # Data could be passed off to another handler here as it doesn't fulfill one of the basi required requests
        pass

    # Kill the socket
    sock.close()
    server.count.decr()

def start_server():
    # # Start the server in async mode
    # server = LithiumAsyncServer('localhost', int(sys.argv[1]), lab2_handler)
    # asyncore.loop()

    # Start the server in thread pool mode
    server = LithiumThreadPoolServer('localhost', int(sys.argv[1]), lab2_handler)
    server.loop()

if __name__ == '__main__':
    start_server()