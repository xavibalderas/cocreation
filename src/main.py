from flask import Flask
import time
from picamera import PiCamera


app = Flask(__name__)

camera = PiCamera()
camera.resolution = (800,600)
camera.start_preview();
time.sleep(5)

@app.route('/')
def hello_world():
	camera.capture('/data/image.jpg')
	print "new photo"
	return send_from_directory('/data', 'image.jpg')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)