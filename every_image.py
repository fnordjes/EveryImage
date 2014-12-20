#!/usr/bin/python

from multiprocessing import Process, Value, Array
import atexit
import Image
import os
import StringIO
import SimpleHTTPServer
import SocketServer
import base64
import pickle
import time

# globals
img = Image.new( 'L', (256,256), "black") # create a new black image
img_pixels = img.load() # create the pixel map

saved_state_filename = './every_image_state.pkl'
store_result = Value('H', False) # flag is set in http request handler
result_ready = Value('H', False) # flag is read by the http request handler
current_permutation = Array('H', [0]*256*256)

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
    #for p in pixels:
    #    average += float(p) - average
    return average

# Save and and resume state on exit and start.
@atexit.register
def save_state():
    print "Saving state."
    write(list(current_permutation), saved_state_filename)

def resume_state(filename):
    data = read(filename)
    if data == None:
        print "Creating new pixel array."
        data = [0] * (256 * 256)
    else:
        print "Restoring pixel array from last run."
        pass
    return data

# The main work is done here - permuting the pixels.
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


def create_every_image(store, ready, current_permutation):

    pixels = list(current_permutation)

    if not os.path.exists(saved_state_filename):
        f = open(saved_state_filename, 'w')
        f.close
    pixels = resume_state(saved_state_filename)

    while pixels[0] < 256:
        for result in permute_in_place(pixels):
            if store.value:
                # copy the reference
                for i, value in enumerate(result):
                    current_permutation[i] = value
	    	    store.value = False
	    	    ready.value = True
        pixels[0] += 1

def write_image():
    for y in range(256):
        for x in range(256):
            img_pixels[x,y] = current_permutation[y * 256 + x]



class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
    
        global store_result
        global result_ready

        store_result.value = True
        while not result_ready.value:
            print "waiting"
            time.sleep(1)
        
        result_ready.value = False
        
        # write the current permutation to pixel array and save image to 
        # string.
        write_image()
        output = StringIO.StringIO()
        img.save(output, format='PNG')
        imgString = output.getvalue()
        output.close()
        response = '<!DOCTYPE html><html><head></head><body><img src="data:image/png;base64,%s" /> </body></html>' % base64.b64encode(imgString)
    
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)
        
        print calc_average()



if __name__ == '__main__':
    
    worker = Process(target=create_every_image, args=(store_result, result_ready, current_permutation))
    worker.start()
    
    Handler = MyRequestHandler
    server = SocketServer.TCPServer(('0.0.0.0', 8888), Handler)
    #print "Starting Server"
    server.serve_forever()
    worker.join()

# we never get here
        





