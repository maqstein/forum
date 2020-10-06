import linecache
import sys


class Error(Exception):
    """Base class for other exceptions"""
    pass


class NoArgumentsPassedError(Error):
    """Raised when you pass no arguments to a function"""


def GetExceptionInfo():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    text = f'EXCEPTION IN {filename},LINE {lineno},"{line.strip()}" {exc_obj}, '
    
    return text


def BasicExceptionHandler(func):
    def inner_func(*args,**kwargs):
        try:
            func(*args,**kwargs)
        except:
            # TODO add Logger support
            print(GetExceptionInfo())
    return inner_func