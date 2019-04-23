import time
import logging
from django.core.cache import caches
from django.utils.encoding import smart_str
import hashlib

# Get an instance of a logger
logger = logging.getLogger('django')

# Get the specific cache for expensive function storing
cache = caches['expensive']


def _smart_key(key):
    return smart_str(''.join([c for c in key if ord(c) > 32 and ord(c) != 127]))


def _build_cachekey(func_name, func_args, func_kwargs):
    ka = str((func_args, tuple(sorted(func_kwargs.items()))))
    return '%s.%s' % (func_name, hashlib.md5(_smart_key(ka).encode('utf-8')).hexdigest())


def make_key(key, key_prefix, version):
    "Truncate all keys to 250 or less and remove control characters"
    return ':'.join([key_prefix, str(version), _smart_key(key)])[:250]


def vary_on_leaguedata(func):
    def func_wrapper(*args, **kwargs):
        key = make_key(_build_cachekey(func.__qualname__, args, kwargs), '', 1)
        cached = cache.get(key)
        if cached is None:
            cached = func(*args, **kwargs)
            cache.set(key, cached, None)  # no timeout: cache flushé par le prochain computescores
            # qui aura des données récentes à processer.
        return cached

    return func_wrapper


def flush_expensive_cache_before(func):
    def func_wrapper(*args, **kwargs):
        flush_cache()
        return func(*args, **kwargs)

    return func_wrapper


def flush_cache():
    cache.clear()
