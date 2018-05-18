from flask import Flask, render_template
import time
from picamera import PiCamera


app = Flask(__name__)

camera = PiCamera()
camera.resolution = (800,600)
camera.start_preview();
time.sleep(5)

@app.route('/')
def hello_world():
	camera.capture('img/image.jpg')
	print "new photo"
	return render_template('hello.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)