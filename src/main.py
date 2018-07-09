# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory
import time
from datetime import datetime
from picamera import PiCamera


app = Flask(__name__)

camera = PiCamera()
camera.resolution = (800,600)
camera.start_preview()
time.sleep(5)
photos_captured = 0

@app.route('/')
def make_photo():
	camera.capture('image.jpg')
	photos_captured = photos_captured + 1
	print '>>Captured Photo N° '+ str(photos_captured)
	return send_from_directory('/src/img', 'image.jpg')

@app.route('/test')
def test_render():
	return render_template('test.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html')

@app.errorhandler(500)
def internal_error(error):
	print error
	return render_template('internal_error.html')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
