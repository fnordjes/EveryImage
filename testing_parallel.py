#!/usr/bin/python

from multiprocessing import Process, Value, Array
import os

ready = Value('H', True)
store = Array('H', range(10))

def info(title):
    print title
    print 'module name:', __name__
    if hasattr(os, 'getppid'):  # only available on Unix
        print 'parent process:', os.getppid()
    print 'process id:', os.getpid()

def f(name, boo, store):
    info('function f')
    boo.value = False
    store[0] += 1
    print 'hello', name

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',ready, store))
    
    print store[0]
    p.start()
    p.join()
    print ready.value
    print store[0]
