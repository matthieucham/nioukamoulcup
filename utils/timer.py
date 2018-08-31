import time
from django.conf import settings


def timed(func):
    def func_wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            secs = end - start
            msecs = secs * 1000  # millisecs
            if settings.DEBUG:
                print('elapsed time for %s: %f ms' % (func.__name__, msecs))

    return func_wrapper
