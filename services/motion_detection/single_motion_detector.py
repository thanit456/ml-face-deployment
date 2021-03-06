import numpy as np
import imutils
import cv2
from services.detector import Detector


class SingleMotionDetector(Detector):
    def __init__(self, accumWeight=0.5):
        super().__init__()
        self.accumWeight = accumWeight
        self.bg = None

    def get_name(self):
        return "Single motion detection"

    def update(self, image):
        if self.bg is None:
            self.bg = (image.copy()).astype('float')
            return
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, thresh_value=25):

        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, thresh_value, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # print('Contours : ',cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        if len(cnts) == 0:
            return None

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x), max(maxY, y))

        return (thresh, (minX, minY, maxX, maxY))
