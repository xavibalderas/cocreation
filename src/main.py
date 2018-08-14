# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, request
import time
import cups
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
#camera.start_preview()
time.sleep(2)

# At GET, we make a photo and then we display it.
@app.route('/')
def make_photo():
	camera.capture('image.jpg')
	print '>>Captured Photo'
	# Use 'as_attachment=True' as another parameter of send_file() if you want to serve the download instead of just displaying the pic.
	return send_file('image.jpg')

# Testing view
@app.route('/test')
def test_render():
	return render_template('test.html')

@app.route('/print_pdf', methods=['POST','GET'] )
def print_pdf():
	
	if request.method == 'GET':
		# First we snap a picture
		camera.capture('image.jpg',resize=(640,480))
		# We gather the material name from the url arguments
		nameMaterial = request.args.get('data',default = '', type = str)
		
		# Start PDF 
		pdf = FPDF('L','in',(5,7))
		pdf.add_font('verdana','', fname='/usr/share/fonts/TTF/verdana.ttf',uni=True)
		
		print '>>DEBUG: Pdf created.'

		pdf.add_page()

		pdf.image('image.jpg',w=2,h=2)
		pdf.set_font('Verdana',size=14)
		pdf.cell(w=1,h=1,txt=nameMaterial)
		
		pdf.output('test.pdf','F')
		print '>>DEBUG: End reach.'
		
		# Get printer and print PDF
		cups_handler = cups.Connection()
		printers = cups_handler.getPrinters()
		print '>>DEBUG: Searching printers...'
		for printer in printers:
			print printer, printers[printer]["device-uri"]
		
		print '>>DEBUG: Sending pdf to first printer.'
		printer_id=printers.keys()[0]
		cups_handler.printFile(printer_id,'test.pdf',"Test",{})
		print '>>DEBUG: File sent.'
	
		# Serve PDF	
		return send_file('test.pdf')
		
	return render_template('page_not_found.html')

@app.route('/download_pdf', methods=['POST','GET'] )
def download_pdf():
	
	if request.method == 'GET':
		# First we snap a picture
		camera.capture('image.jpg',resize=(1280,720))
		# We gather the material name from the url arguments
		nameMaterial = request.args.get('data',default = '', type = str)
		
		# Start PDF 
		pdf = FPDF('L','in',(5,7))
		pdf.add_font('verdana','', fname='/usr/share/fonts/TTF/verdana.ttf',uni=True)
		pdf.set_auto_page_break('false',margin=0.0);
		print '>>DEBUG: Pdf created.'
		pdf.add_page()


		pdf.image('image.jpg',w=4,h=4)
		pdf.set_font('Verdana',size = 14)
		pdf.cell(4,1,txt=nameMaterial,fill='True')


		pdf.output('test.pdf','F')
		print '>>DEBUG: End reach.'
	
		# Serve PDF	
		return send_file('test.pdf')
		
	return render_template('page_not_found.html')

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

    app.run(host='0.0.0.0', port=8088)
