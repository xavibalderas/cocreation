#!/usr/bin/python

import time
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (2592,1944)
camera.start_preview();
time.sleep(5)
count = 1
while True:
	camera.capture('/data/image' + str(count) + '.jpg')
	print "New picture"
	count = count + 1
	time.sleep(10)
	

camera.stop_preview();