import linecache
import sys


class Error(Exception):
    """Base class for other exceptions"""
    pass


class NoArgumentsPassedError(Error):
    """Raised when you pass no arguments to a function"""


def get_exception_info():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    line_number = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_number, f.f_globals)
    text = f'EXCEPTION IN {filename},LINE {line_number},"{line.strip()}" {exc_obj}, '

    return text


def get_basic_exception_handler(func):
    def inner_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            # TODO add Logger support
            print(get_exception_info())

    return inner_func
