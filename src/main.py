from flask import Flask, render_template, send_from_directory
import time
from picamera import PiCamera


app = Flask(__name__)

camera = PiCamera()
camera.resolution = (800,600)
camera.start_preview();
time.sleep(5)

@app.route('/')
def hello_world():
	camera.capture('src/img/image.jpg')
	print "new photo"
	return send_from_directory('img', 'image.jpg')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)