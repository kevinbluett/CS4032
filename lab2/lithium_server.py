import asyncore, socket, errno
from socket import timeout as SocketTimeout, error as SocketError
from lithium_threading import *

class LithiumHelper(object):
    @staticmethod
    def recv_all(socket):
        read = ''
        if 1:
            try :
                data = socket.recv(1024)
                read += data
            except SocketError, e:
                if isinstance(e.args, tuple):
                    if e[0] == errno.EPIPE:
                       # remote peer disconnected
                       print "Detected remote disconnect"
                    else:
                       # determine and handle different error
                       pass
                else:
                    print "socket error ", e
                # break
            except IOError, e:
                # Hmmm, Can IOError actually be raised by the socket module?
                print "Got IOError: ", e
                # break
        return read

def process_input(socket):
    input = LithiumHelper.recv_all(socket)
    socket.send(input)

class LithiumHandler(asyncore.dispatcher):

    def __init__(self, pool, socket):
        self.pool = pool
        self.socket = socket
        asyncore.dispatcher.__init__(self, sock=socket)

    def handle_read(self):
        self.process(self)

    def process(self, dispatcher):
        try:
            self.pool.add_task(process_input, dispatcher.socket)
        except SocketError, e: 
            print e

    def handle_error(self):
        self.close()
        self.pool.add_count(-1)

    def handle_close(self):
        self.close()
        self.pool.add_count(-1)

class LithiumServer(asyncore.dispatcher):

    WORKERS = 10

    def __init__(self, host, port):
        self._pool = LithiumThreadPool(self.WORKERS)
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self._pool.add_count(1)
            print 'Incoming connection from %s, socket count %d' % (repr(addr), self._pool.open_socket_count)
            handler = LithiumHandler(self._pool, sock)

    def shutdown(self):
        if self._pool is not None:
            self._pool.shutdown()

server = LithiumServer('localhost', 8000)
asyncore.loop()

# if __name__ == '__main__':
#     from random import randrange
#     delays = [randrange(1, 10) for i in range(100)]
    
#     from time import sleep
#     def wait_delay(d):
#         print 'sleeping for (%d)sec' % d
#         sleep(d)
    
#     # 1) Init a Thread pool with the desired number of threads
#     pool = ThreadPool(20)
    
#     for i, d in enumerate(delays):
#         # print the percentage of tasks placed in the queue
#         print '%.2f%c' % ((float(i)/float(len(delays)))*100.0,'%')
        
#         # 2) Add the task to the queue
#         pool.add_task(wait_delay, d)
    
#     # 3) Wait for completion
#     pool.wait_completion()