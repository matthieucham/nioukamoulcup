import time
import logging
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger('django')


def timed(func):
    def func_wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            secs = end - start
            msecs = secs * 1000  # millisecs
            logger.debug('elapsed time for %s: %f ms' % (func.__name__, msecs))

    return func_wrapper
