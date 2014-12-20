#!/usr/bin/python

import atexit
import os
import pickle
from array import array
import time

def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

def permute_in_place(a):
    a.sort()
    yield list(a)

    if len(a) <= 1:
        return

    first = 0
    last = len(a)
    while 1:
        i = last - 1

        while 1:
            i = i - 1
            if a[i] < a[i+1]:
                j = last - 1
                while not (a[i] < a[j]):
                    j = j - 1
                a[i], a[j] = a[j], a[i] # swap the values
                r = a[i+1:last]
                r.reverse()
                a[i+1:last] = r
                yield list(a)
                break
            if i == first:
                a.reverse()
                return

#current = []
#def test2():
#    for result in permute_in_place(range(10)):
#        current = result
#    print current


def write(data, outfile):
    try:
        f = open(outfile, "w+b")
        try:
            pickle.dump(data, f)
        finally:
            f.close()
    except IOError:
        pass 


def read(filename):
    data = None
    try:
        f = open(filename)
        try:
            data = pickle.load(f)
        except:
            pass
        finally:
            f.close()
    except IOError:
        pass
    return data

def calc_average():
    average = 0.0
    for p in pixels:
        average += float(p) - average
    return average

#@atexit.register
def save_state():
    print "Saving state."
    write(current, filename)

def resume_state(filename):
    data = read(filename)
    if data == None:
        print "Creating pixel array."
        #data = [0] * 10 #* (256 * 256)
        
        data = range(256) * (256 * 256)
        data[0] = 1
    else:
        print "Restoring pixel array from last run."
    return data

# globals (being lazy and using atexit with a decorator (no arguments for save_state() ))
current = []
filename = './every_image_state.pkl'

if __name__ == '__main__':
    #import timeit
    #print(timeit.timeit("test2()", setup="from __main__ import test2", number=1))

    
    #if not os.path.exists(filename):
    #    f = open(filename, 'w')
    #    f.close
    #pixels = resume_state(filename)
    pixels = range(10)

    t = time.time()

    store_result = True
    #store_result = False
    
    #while pixels[0] < 10: #256:
    count = 0
    for result in permute_in_place(pixels):
        count += 1
        if store_result:
            pass
    	    #print list(result)
    	    

    	    
    print "time taken list: ", time.time() -t
    print "count", count
    print
    t = time.time()
      	    


    a = array('H', pixels)	    
    count = 0
    for result in permutations(a):
        count += 1
        if store_result:
            pass
    	    #print list(result)
    	    

    #    pixels[0] += 1
    
    
    print "time taken array: ", time.time() -t
    print "done"
    print "average", calc_average()
    print "count", count

    #print current



