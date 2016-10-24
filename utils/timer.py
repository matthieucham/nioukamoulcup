import time


class Timer():
    def __init__(self, id='timer', verbose=False):
        self.verbose = verbose
        self.id = id

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print('elapsed time for %s: %f ms' % (self.id, self.msecs))
