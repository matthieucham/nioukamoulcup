import time
from functools import wraps
from django.utils.decorators import ContextDecorator


class Timer(object):
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

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner


class TimerDecorator(object):
    def __init__(self, f):
        self.f = f
        wraps(f)(self)

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.f(*args, **kwargs)
        end = time.time()
        msecs = (end - start) * 1000
        print('elapsed time for %s: %f ms' % (self.f.__name__, msecs))
        return result
