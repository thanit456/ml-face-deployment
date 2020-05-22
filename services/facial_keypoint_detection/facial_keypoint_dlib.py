import dlib
import numpy as np
import cv2
import imutils
from imutils import face_utils

from services.detector import Detector
# https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
# ! have to restructure code for ease of use


class DLibFacialKeyPointDetector(Detector):
    def __init__(self, shape_detector_path):
        super().__init__()
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_detector_path)
        self.facial_keypoints = []

    def get_name(self):
        return 'DLib facial keypoint detector'
    # def rect2bb(rect):
    #     x = rect.left()
    #     y = rect.top()
    #     w = rect.right() - x
    #     h = rect.bottom() - y
    #     return (x, y, w, h)

    # def shape2np(shape, dtype='int'):
    #     coords = np.zeros((68, 2), dtype=dtype)
    #     for i in range(0, 68):
    #         coords[i] = (shape.part(i).x, shape.part(i).y)
    #     return coords

    def detect(self, image):
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = self.detector(gray, 1)

        self.facial_keypoints = []

        for i, rect in enumerate(rects):
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(rect)

            (x, y, w, h) = face_utils.rect_to_bb(rect)

            self.facial_keypoints.append((x, y, w, h, shape))
        return self.facial_keypoints

    def draw(self, image):
        for i, (x, y, w, h, shape) in enumerate(self.facial_keypoints):
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, "Face {}".format(i), (x-10, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            for (x, y) in shape:
                cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
        return image
