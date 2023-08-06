# This file is placed in the Public Domain.


"executables"


import os
import sys
import termios
import time
import traceback


def cprint(*args):
    print(*args)
    sys.stdout.flush()


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def from_exception(ex, txt="", sep=" "):
    result = []
    for fr in traceback.extract_tb(ex.__traceback__):
        fnc = str(fr).split()[-1][:-1]
        nme = os.sep.join(fr.filename.split(os.sep)[-2:])
        result.append("%s %s.%s" % (nme, fnc, fr.lineno))
    return "%s -> %s -> %s" % (getname(ex), " -> ".join(result), ex)


def getname(o):
    t = type(o)
    if isinstance(t, types.ModuleType):
        return o.__name__
    if "__self__" in dir(o):
        return "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    if "__class__" in dir(o) and "__name__" in dir(o):
        return "%s.%s" % (o.__class__.__name__, o.__name__)
    if "__class__" in dir(o):
        return o.__class__.__name__
    if "__name__" in dir(o):
        return o.__name__
    return None


def wait():
    while 1:
        time.sleep(1.0)


def wrap(func):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        cprint("")
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
