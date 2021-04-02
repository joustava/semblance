import cv2
import numpy


def bbox(image):
    ret, tresh = cv2.threshold(cv2.cvtColor(
        image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)

    contours, hier = cv2.findContours(
        tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)


def minimumarea(image):
    ret, tresh = cv2.threshold(cv2.cvtColor(
        image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)

    contours, hier = cv2.findContours(
        tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        cv2.drawContours(image, [box], 0, (0, 0, 255), 3)

class CircleDetector:
    def detect(self, image):
        ret, tresh = cv2.threshold(cv2.cvtColor(
            image, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)

        contours, hier = cv2.findContours(
            tresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(image, center, radius, (0, 255, 0), 2)
        
        return image
