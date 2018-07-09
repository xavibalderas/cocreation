# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file
import time
from picamera import PiCamera


app = Flask(__name__)

# Let's load the camera. We're using the V2 PiCamera:
# Accepted resolutions for maximum FoV: 
# 3280x2464 (4:3)
# 1640x1232 (4:3)
# 1640x922  (16:9)
# 1280x720  (16:9)
# 640x480   (4:3)
camera = PiCamera()
camera.resolution = (3280,2464)
camera.start_preview()
time.sleep(5)

# At GET, we make a photo and then we display it.
@app.route('/')
def make_photo():
	camera.capture('image.jpg')
	print '>>Captured Photo'
	# Use 'as_attachment=True' as another parameter of send_file() if you want to serve the download in the browser
	return send_file('/usr/src/app/image.jpg')

# Testing view
@app.route('/test')
def test_render():
	return render_template('test.html')
# 404 handler
@app.errorhandler(404)
def page_not_found(error):
	print error
	return render_template('page_not_found.html')
# 500 handler
@app.errorhandler(500)
def internal_error(error):
	print error
	return render_template('internal_error.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
