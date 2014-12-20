#!/usr/bin/python

from PIL import Image

pixels = range(256) * 256
print len(pixels)
img = Image.new( 'L', (256,256), "black") # create a new black image
img_pixels = img.load()
#img.save('./black.png')

for y in range(256):
    for x in range(256):
        img_pixels[x,y] = pixels[y * 256 + x]




img.save('./black.png')