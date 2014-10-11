import asyncore
from helpers import *

class LithiumHandler(asyncore.dispatcher):
    def __init__(self, server, pair):
        self.pair = pair
        self.server = server
        asyncore.dispatcher.__init__(self, sock=pair[0])

    def handle_read(self):
        self.process(self)

    def process(self, dispatcher):
        self.server.handler(self.server, (self, self.pair[1]))

    def handle_error(self):
        self.close()
        self.server.count.decr()

    def handle_close(self):
        self.close()
        self.server.count.decr()

class LithiumAsyncServer(asyncore.dispatcher):

    MAX_CONNECTIONS = 2000

    def __init__(self, host, port, handler):
        self.count = AtomicCount()
        self.handler = handler
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

        print "Starting Lithuim async server"
        print "Listening on %s:%d" % (host, port)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.count.incr()
            print 'Incoming connection from %s, socket count %d' % (repr(addr), self.count.count)
            if self.count.count > self.MAX_CONNECTIONS:
                sock.send("503 - Service unavailable\n")
                sock.close()
                self.count.decr()
            else:
                handler = LithiumHandler(self, pair)

    def shutdown(self, safe = True):
        if safe and self.pool is not None:
            self.pool.shutdown()
        self.close()
        asyncore.close_all()