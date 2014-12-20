#!/usr/bin/python


from copy import deepcopy

class old_class:
    def __init__(self):
        self.blah = 'blah'

class new_class(object):
    def __init__(self):
        self.blah = 'blah'

dignore = {str: None, unicode: None, int: None, type(None): None}

def Copy(obj, use_deepcopy=True):
    t = type(obj)

    if t in (list, tuple):
        if t == tuple:
            # Convert to a list if a tuple to 
            # allow assigning to when copying
            is_tuple = True
            obj = list(obj)
        else: 
            # Otherwise just do a quick slice copy
            obj = obj[:]
            is_tuple = False

        # Copy each item recursively
        for x in xrange(len(obj)):
            if type(obj[x]) in dignore:
                continue
            obj[x] = Copy(obj[x], use_deepcopy)

        if is_tuple: 
            # Convert back into a tuple again
            obj = tuple(obj)

    elif t == dict: 
        # Use the fast shallow dict copy() method and copy any 
        # values which aren't immutable (like lists, dicts etc)
        obj = obj.copy()
        for k in obj:
            if type(obj[k]) in dignore:
                continue
            obj[k] = Copy(obj[k], use_deepcopy)

    elif t in dignore: 
        # Numeric or string/unicode? 
        # It's immutable, so ignore it!
        pass 

    elif use_deepcopy: 
        obj = deepcopy(obj)
    return obj

if __name__ == '__main__':
    import copy
    from time import time

    num_times = 1000
    #L = [None, 'blah', 1, 543.4532, ['foo'], ('bar',), {'blah': 'blah'},
    #     old_class(), new_class()]
    L = range(256 * 256)

    t = time()
    for i in xrange(num_times):
        Copy(L)
    print 'Custom Copy:', time()-t

    t = time()
    for i in xrange(num_times):
        Copy(L, use_deepcopy=False)
    print 'Custom Copy Only Copying Lists/Tuples/Dicts (no classes):', time()-t

    t = time()
    for i in xrange(num_times):
        copy.copy(L)
    print 'copy.copy:', time()-t

    t = time()
    for i in xrange(num_times):
        copy.deepcopy(L)
    print 'copy.deepcopy:', time()-t

    t = time()
    for i in xrange(num_times):
        L[:]
    print 'list slicing [:]:', time()-t

    t = time()
    for i in xrange(num_times):
        list(L)
    print 'list(L):', time()-t

    t = time()
    for i in xrange(num_times):
        [i for i in L]
    print 'list expression(L):', time()-t

    t = time()
    for i in xrange(num_times):
        a = []
        a.extend(L)
    print 'list extend:', time()-t

    t = time()
    for i in xrange(num_times):
        a = []
        for y in L:
            a.append(y)
    print 'list append:', time()-t

    t = time()
    for i in xrange(num_times):
        a = []
        a.extend(i for i in L)
    print 'generator expression extend:', time()-t

