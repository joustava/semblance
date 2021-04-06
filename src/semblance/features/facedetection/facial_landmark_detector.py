from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2


# Download model to same dir first and unzip
# dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
class FacialLandmarkDetector:
    def __init__(self, confidence=0.5):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("src/semblance/features/facedetection/shape_predictor_68_face_landmarks.dat")
        
    
    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 1)

        for (i, rect) in enumerate(rects):
          # determine the facial landmarks for the face region, then
          # convert the facial landmark (x, y)-coordinates to a NumPy
          # array
          shape = self.predictor(gray, rect)
          shape = face_utils.shape_to_np(shape)
          # convert dlib's rectangle to a OpenCV-style bounding box
          # [i.e., (x, y, w, h)], then draw the face bounding box
          (x, y, w, h) = face_utils.rect_to_bb(rect)
          cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
          # show the face number
          cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
          # loop over the (x, y)-coordinates for the facial landmarks
          # and draw them on the frame
          for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
          
        return frame

