import dlib
import numpy as np
import cv2
import imutils

# https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
# ! Incomplete detect and have to restructure code for ease of use


class DLibFacialKeyPointDetector:
    def __init__(self, shape_detector_path):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_detector_path)

    def rect2bb(rect):
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y
        return (x, y, w, h)

    def shape2np(shape, dtype='int'):
        coords = np.zeros((68, 2), dtype=dtype)
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords

    def detect(image):
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = self.detector(gray, 1)

        for i, rect in enumerate(rects):
            shape = self.predictor(gray, rect)
            shape = shape2np(rect)

        (x, y, w, h) = rect2bb(rect)
