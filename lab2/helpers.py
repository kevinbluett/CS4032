__author__ = 'kevin'
import socket
from threading import Lock

class LithiumHelper(object):
    @staticmethod
    def recv_all(sock):
        read = ''
        try:
            data = sock.recv(1024)
            read += data
        except socket.error, e:
            if isinstance(e.args, tuple):
                if e[0] == socket.errno.EPIPE:
                   print "Detected remote disconnect"
                   raise e
            else:
                print "socket error ", e
        return read

class AtomicCount(object):
    def __init__(self):
        self.count = 0
        self.lock = Lock()

    def incr(self):
        self._add_count(1)

    def decr(self):
        self._add_count(-1)

    def _add_count(self, value):
        self.lock.acquire()
        self.count += value
        self.lock.release()