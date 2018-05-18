from flask import Flask
import time
from picamera import PiCamera


app = Flask(__name__)



@app.route('/')

def hello_world():
	camera = PiCamera()
	camera.resolution = (800,600)
	time.sleep(2)
	camera.capture('/data/image.jpg')
	return send_file('/data/image.jpg')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)