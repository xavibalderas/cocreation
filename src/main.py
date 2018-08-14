# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file
import time
from picamera import PiCamera
from fpdf import FPDF


app = Flask(__name__)

# Let's load the camera. We're using the V2 PiCamera:
# Accepted resolutions for maximum FoV: 
# 3280x2464 (4:3)
# 1640x1232 (4:3)
# 1640x922  (16:9)
# 1280x720  (16:9)
# 640x480   (4:3)
camera = PiCamera()
camera.resolution = (1280,720)
camera.start_preview()
time.sleep(2)

# At GET, we make a photo and then we display it.
@app.route('/')
def make_photo():
	camera.capture('image.jpg')
	print '>>Captured Photo'
	# Use 'as_attachment=True' as another parameter of send_file() if you want to serve the download instead of just displaying the pic.
	return send_file('/usr/src/app/image.jpg')

# Testing view
@app.route('/test')
def test_render():
	return render_template('test.html')

@app.route('/pdf')
def create_pdf():

	camera.capture('image.jpg',resize=(1280,960))
	pdf = FPDF('L','in',(5,7))
	print '>>DEBUG: Pdf created.'
	pdf.add_page()
	pdf.image('image.jpg')
	print '>>DEBUG: Image added.'
	pdf.output('test.pdf','F')
	print '>>DEBUG: End reach.'
	return send_file

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
