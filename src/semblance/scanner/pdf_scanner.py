import numpy as np
import imutils
from imutils import perspective
from imutils import contours
import cv2
from scipy.spatial import distance
from contours.canny_edge_detector import CannyEdgeDetector
from filters.edge.canny import apply
class PDFScanner:
  def __init__(self):
    self.edge_detector = CannyEdgeDetector()
  

  def detect(self, image):
    return self.detect_edges(image)

  def detect_edges(self, image):
    # ratio = image.shape[0] / 800.0
    # edge detection and edge enhancements
    # edged = self.edge_detector.detect(image)
    edged = apply(image)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    # contours from edges
    ctrs = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ctrs = imutils.grab_contours(ctrs)
    (ctrs, _) = contours.sort_contours(ctrs)
  

    targets = []

    for c in ctrs[:1]:
      peri = cv2.arcLength(c, True)
      approx = cv2.approxPolyDP(c, 0.02 * peri, True)

      if(len(approx) == 4):
        targets.append(approx)
    

    if(len(targets) > 0):
      return perspective.four_point_transform(image, targets[0].reshape(4, 2))
    else:
      return image

# def order(self, points):
#   # return sorted(points, key=lambda k: [k[0], k[1]])
#   # sort the points based on their x-coordinates
#   xSorted = points[np.argsort(points[:, 0]), :]
#   # grab the left-most and right-most points from the sorted
#   # x-roodinate points
#   leftMost = xSorted[:2, :]
#   rightMost = xSorted[2:, :]
#   # now, sort the left-most coordinates according to their
#   # y-coordinates so 
# 
# we can grab the top-left and bottom-left
#   # points, respectively
#   leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
#   (tl, bl) = leftMost
#   # now that we have the top-left coordinate, use it as an
#   # anchor to calculate the Euclidean distance between the
#   # top-left and right-most points; by the Pythagorean
#   # theorem, the point with the largest distance will be
#   # our bottom-right point
#   D = distance.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
#   (br, tr) = rightMost[np.argsort(D)[::-1], :]
#   # return the coordinates in top-left, top-right,
#   # bottom-right, and bottom-left order
#   return np.array([tl, tr, br, bl], dtype="float32")

