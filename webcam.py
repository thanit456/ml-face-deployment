import cv2
from motion_detection.single_motion_detector import SingleMotionDetector

class Webcam(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    def getFrame(self):
        success, image = self.video.read()
        
        ret, jpeg  = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def getMotionDetectionFrame(self, total, frameCount=32):
        success, image = self.video.read()
        
        # # preparing for ease of detecting motion
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # # motion detection
        # motion_detector = SingleMotionDetector(accumWeight=0.1)
        # detected_gray = motion_detector.detect(gray)

        # if total > frameCount: 
            
        #     if detected_gray is not None:
        #         (thresh, (minX, minY, maxX, maxY)) = detected_gray
        #         print('Coords : ', minX, minY, maxX, maxY)
        #         cv2.rectangle(image, (minX, minY), (maxX, maxY), (0, 0, 255), 2)
        
        # if detected_gray is not None:
        #     detected_gray.update(gray)
        # total += 1

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
