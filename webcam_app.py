from flask import Flask, render_template, Response
from webcam import Webcam

import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def genCamera(camera):
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(genCamera(Webcam()),
            mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)