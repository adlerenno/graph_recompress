from timeit import time
from contextlib import contextmanager

from evaluate.timetest import log


def timing(f):
    """a wrapper to stop the time of a single function."""
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        log('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


@contextmanager
def timeit_context(name):
    """Can be used to stop the time with an 'with ... as ...' block."""
    start_time = time.time()
    yield
    elapsed_time = time.time() - start_time
    log('[{}] finished in {} ms'.format(name, int(elapsed_time * 1000)))


def time_function(f, *args, **kwargs):
    """stops the time of a single function. returns the return value of the function and the time needed."""
    start_time = time.time()
    ret = f(*args, **kwargs)
    elapsed_time = time.time() - start_time
    return ret, elapsed_time
