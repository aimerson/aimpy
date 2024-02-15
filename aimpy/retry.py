
import time
import functools
import traceback
from sync_logging import Logging

def retry(retry_num, retry_sleep_sec,raiseException):
    def decorator(func):
        """decorator"""
        # preserve information about the original function, or the func name will be "wrapper" not "func"
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper"""
            for attempt in range(retry_num):
                try:
                    return func(*args, **kwargs)  # should return the raw function's return value
                except Exception as err:   # pylint: disable=broad-except
                    Logging.log(str(err))
                    time.sleep(retry_sleep_sec)
                Logging.log("RETRY: {0}: Trying attempt {1} of {2}.".format(func.__qualname__, attempt+1, retry_num))
            Logging.log("RETRY: attempt {0} retry failed".format(func.__qualname__))
            if raiseException:
                raise Exception('RETRY: Exceed max retry num: {0} failed'.format(retry_num))
        return wrapper
    return decorator