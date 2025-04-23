#! /usr/bin/env python

import functools

def catch_all_and_print(f):
    """
    A function wrapper for catching all exceptions and logging them
    """
    @functools.wraps(f)
    def inner(*args, **kwargs): 
        try:
            return f(*args, **kwargs)
        except Exception as ex:
            print(ex)
        return inner 