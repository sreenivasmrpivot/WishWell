# logging_decorator.py

import logging
import functools
import time

class SensitiveData:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "****"

def log_entry_exit(entry_level=logging.DEBUG, exit_level=logging.INFO, log_args=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if log_args:
                args_repr = [repr(a) if not isinstance(a, SensitiveData) else repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" if not isinstance(v, SensitiveData) else f"{k}={repr(v)}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                logging.log(entry_level, f"Entering: {func.__name__}({signature})")
            else:
                logging.log(entry_level, f"Entering: {func.__name__}")

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                logging.log(exit_level, f"Exiting: {func.__name__} after {end_time - start_time:.2f} seconds")
        return wrapper
    return decorator

def auto_log_entry_exit(exclude=None):
    if exclude is None:
        exclude = []

    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and attr_name not in exclude:
                setattr(cls, attr_name, log_entry_exit()(attr_value))
        return cls

    return class_decorator
