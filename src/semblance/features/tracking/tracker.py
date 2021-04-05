import cv2
import imutils
import numpy as np
from collections import deque

class TennisBallTracker:
    """
    Tracks an object detected to be in the configured (HSL) color range (a wilson nr4 tennisball by default)
    """
    def __init__(self, lowerRange=(28, 70, 110), upperRange=(53, 147, 226), trailSize=64):
        self._lower = lowerRange
        self._upper = upperRange
        self._points = deque(maxlen=trailSize)

    def detect(self, frame):
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self._lower, self._upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        center = None

        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            
            # find image moment M, to calculate center point of the subject
            M = cv2.moments(contour)
            
            Cx = int(M["m10"] / M["m00"])
            Cy = int(M["m01"] / M["m00"])
            
            center = (Cx, Cy)
            
            # Draw circle and center of subject of interest
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        if(center is not None):
            self._points.appendleft(center)

        # draw trail of tracked subject
        for i in range(1, len(self._points)):
            thickness = int(np.sqrt(self._points.maxlen / float(i + 1)) * 2.5)
            cv2.line(frame, self._points[i - 1], self._points[i], (0, 0, 255), thickness)

        return frame