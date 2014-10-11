from Queue import Queue
from threading import Thread, Lock

class LithiumWorker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            func(*args, **kargs)
            self.tasks.task_done()

class LithiumThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.count_lock = Lock()
        self.open_socket_count = 0
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): LithiumWorker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def shutdown(self):
        """ Wait for tasks to complete """
        self.tasks.join()

    def add_count(self, value):
        """ """
        self.count_lock.acquire()
        self.open_socket_count += value
        print "Count modified %d" % self.open_socket_count
        self.count_lock.release()