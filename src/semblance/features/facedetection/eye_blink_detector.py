from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2


# Download model to same dir first and unzip
# dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
class EyeBlinkDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("src/semblance/features/facedetection/shape_predictor_68_face_landmarks.dat")
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        self.EYE_AR_THRESH = 0.3
        self.EYE_AR_CONSEC_FRAMES = 3
        # initialize the frame counters and the total number of blinks
        self.COUNTER = 0
        self.TOTAL = 0

    def eye_aspect_ratio(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        # return the eye aspect ratio
        return ear

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale frame
        rects = self.detector(gray, 0)

        # loop over the face detections
        for rect in rects:
          # determine the facial landmarks for the face region, then
          # convert the facial landmark (x, y)-coordinates to a NumPy
          # array
          shape = self.predictor(gray, rect)
          shape = face_utils.shape_to_np(shape)
          # extract the left and right eye coordinates, then use the
          # coordinates to compute the eye aspect ratio for both eyes
          leftEye = shape[self.lStart:self.lEnd]
          rightEye = shape[self.rStart:self.rEnd]
          leftEAR = self.eye_aspect_ratio(leftEye)
          rightEAR = self.eye_aspect_ratio(rightEye)
          # average the eye aspect ratio together for both eyes
          ear = (leftEAR + rightEAR) / 2.0

          # compute the convex hull for the left and right eye, then
          # visualize each of the eyes
          leftEyeHull = cv2.convexHull(leftEye)
          rightEyeHull = cv2.convexHull(rightEye)
          cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
          cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

          # check to see if the eye aspect ratio is below the blink
          # threshold, and if so, increment the blink frame counter
          if ear < self.EYE_AR_THRESH:
            self.COUNTER += 1
          # otherwise, the eye aspect ratio is not below the blink
          # threshold
          else:
            # if the eyes were closed for a sufficient number of
            # then increment the total number of blinks
            if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
              self.TOTAL += 1
            # reset the eye frame counter
            self.COUNTER = 0

          # draw the total number of blinks on the frame along with
          # the computed eye aspect ratio for the frame
          cv2.putText(frame, "Blinks: {}".format(self.TOTAL), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
          cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
      
        return frame