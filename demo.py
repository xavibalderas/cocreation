#!/usr/bin/python

import time
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (320, 240)
camera.start_preview();
time.sleep(5)
count = 1
while True:
	camera.capture('/data/image' + str(count) + '.jpg')
	print "New picture"
	count = count + 1
	

camera.stop_preview();