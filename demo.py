#!/usr/bin/python

import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    # Camera warm-up time
    time.sleep(2)
    camera.capture('/data/image.jpg')

print 'Picture taken'
count = 1
while True:
	picamera.PiCamera().capture('/data/image' + count + '.jpg')
	print "New picture"
	time.sleep(10)