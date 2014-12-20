#!/usr/bin/python

import Image
import StringIO
import SimpleHTTPServer
import SocketServer
import time
import base64


img = Image.new( 'RGB', (255,255), "black") # create a new black image
pixels = img.load() # create the pixel map
 
for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # set the colour accordingly
#time.sleep(0.01)


class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):

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



Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)
print "Starting Server"
server.serve_forever()

# we never get here
        
imgSize = img.size
rawData = img.tostring()
img = Image.fromstring('RGB', imgSize, rawData)
img.save('rgbmode.png')
#img = Image.fromstring('RGBX', imgSize, rawData)
#img.save('rgbxmode.jfif')
#img = Image.fromstring('RGBA', imgSize, rawData)
#img.save('rgbamode.png')
#img = Image.fromstring('CMYK', imgSize, rawData)
#img.save('rgbamode.tiff')




