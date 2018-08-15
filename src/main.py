# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, request
import time
import cups
from picamera import PiCamera
from fpdf import FPDF

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color,black,white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import BaseDocTemplate, Paragraph, PageTemplate, Frame
from reportlab.pdfbase.pdfmetrics import stringWidth


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
		camera.capture('image.jpg',resize=(1280,720))
		# We gather the names of the materials from the url arguments
		num_args = len(request.args)
		materials = []
		for i in range(num_args):
			materials.append(request.args.get('value' + str(i+1),default = '', type = str))
				
		################################################################
		# Start PDF with ReporLab module
		# Prepare fonts
		pdfmetrics.registerFont(TTFont('Verdana','verdana.ttf'))
		# Static components
		def draw_static(canvas,doc):
			canvas.saveState()
			canvas.setFont('Verdana',8)
			canvas.drawImage('image.jpg',0,0,600,400)
			canvas.setFillColor(white)
			canvas.rect(28,18,80,12,fill=True,stroke=False)	
			canvas.setFillColor(black)
			canvas.drawString(30,20,'IKEA Spreitenbach')
			canvas.restoreState()
		# Creating the document, adding components
		doc = BaseDocTemplate('material.pdf',pagesize=(7*inch,5*inch))
		# Adding frames
		frames = []
		positions = [330,313,296,279,262,245,228,211,194,177]
		for i in range(num_args):
			textWidth = stringWidth(materials[i],'Verdana',14)
			frames.append(Frame(22, positions[i],(textWidth+20),(18),bottomPadding = 0,topPadding=0, id='material'+str(i+1),showBoundary=0))
		
		template = PageTemplate(id='test',frames=frames,onPage=draw_static)
		doc.addPageTemplates([template])
		# Paragraph styling
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='header',fontName='Verdana',fontSize=14,
								  alignment=TA_CENTER,leading=18,backColor=white))
		# Adding paragraphs
		components = []
		for i in range(num_args):
			components.append(Paragraph(materials[i], styles['header']))

		# Assembling document and storing it.
		doc.build(components)
		# Serve PDF	
		return send_file('material.pdf')
		
	return render_template('page_not_found.html')

@app.route('/download_pdf', methods=['POST','GET'] )
def download_pdf():
	
	if request.method == 'GET':
		# First we snap a picture
		camera.capture('image.jpg',resize=(1280,720))
		# We gather the names of the materials from the url arguments
		num_args = len(request.args)
		materials = []
		for i in range(num_args):
			materials.append(request.args.get('value' + str(i+1),default = '', type = str))
				
		################################################################
		# Start PDF with ReporLab module
		# Prepare fonts
		pdfmetrics.registerFont(TTFont('Verdana','verdana.ttf'))
		# Static components
		def draw_static(canvas,doc):
			canvas.saveState()
			canvas.setFont('Verdana',8)
			canvas.drawImage('image.jpg',0,0,600,400)
			canvas.setFillColor(white)
			canvas.rect(28,18,80,12,fill=True,stroke=False)	
			canvas.setFillColor(black)
			canvas.drawString(30,20,'IKEA Spreitenbach')
			canvas.restoreState()
		# Creating the document, adding components
		doc = BaseDocTemplate('material.pdf',pagesize=(7*inch,5*inch))
		# Adding frames
		frames = []
		positions = [330,313,296,279,262,245,228,211,194,177]
		for i in range(num_args):
			textWidth = stringWidth(materials[i],'Verdana',14)
			frames.append(Frame(22, positions[i],(textWidth+20),(18),bottomPadding = 0,topPadding=0, id='material'+str(i+1),showBoundary=0))
		
		template = PageTemplate(id='test',frames=frames,onPage=draw_static)
		doc.addPageTemplates([template])
		# Paragraph styling
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='header',fontName='Verdana',fontSize=14,
								  alignment=TA_CENTER,leading=18,backColor=white))
		# Adding paragraphs
		components = []
		for i in range(num_args):
			components.append(Paragraph(materials[i], styles['header']))

		# Assembling document and storing it.
		doc.build(components)
		# Serve PDF	
		return send_file('material.pdf')
		
	return render_template('page_not_found.html')

# 404 handler
@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html')
# 500 handler
@app.errorhandler(500)
def internal_error(error):
	return render_template('internal_error.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8088)
