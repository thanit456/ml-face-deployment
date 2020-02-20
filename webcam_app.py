from flask import Flask, render_template, Response
from webcam import Webcam
from motion_detection.single_motion_detector import SingleMotionDetector
import cv2


# OpenCV config
cap = cv2.VideoCapture(0)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def genCamera(camera):
    total = 0 
    frameCount = 32

    motion_detector = SingleMotionDetector(accumWeight=0.1)

    while True:
        # frame = camera.getMotionDetectionFrame(total)

        _, image = cap.read()
                
        # preparing for ease of detecting motion
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # motion detection

        if total > frameCount: 
            
            detected_gray = motion_detector.detect(gray)

            if detected_gray is not None:
                (thresh, (minX, minY, maxX, maxY)) = detected_gray
                print('Coords : ', minX, minY, maxX, maxY)
                cv2.rectangle(image, (minX, minY), (maxX, maxY), (0, 0, 255), 2)
        
        
        motion_detector.update(gray)
        total += 1

        ret, jpeg = cv2.imencode('.jpg', image)


        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(genCamera(Webcam()),
            mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)