import numpy as np
import imutils
from imutils import perspective
from imutils import contours
import cv2
from scipy.spatial import distance
from features.edgedetection.canny_edge_filter import CannyEdgeFilter

class PDFScanner:
  def __init__(self):
    self.canny_edge_filter = CannyEdgeFilter()
    self._kernel = (5, 5)
    self._sigma = 0.4
    self._target = None
    self._area = 0


  def detect(self, image):
    return self.detect_edges(image)


  def detect_edges(self, image):
    edged = self.canny_edge_filter.apply(image)

    ctrs = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if(len(ctrs) > 0):
      self.handle_document(ctrs, image)
    
    return image


  def handle_document(self, ctrs, image):
    (w, h, d) = image.shape
    ctrs = imutils.grab_contours(ctrs)
    cnts = sorted(ctrs, key = cv2.contourArea, reverse = True)[:5]

    document = None
    for c in ctrs:
      peri = cv2.arcLength(c, True)
      approx = cv2.approxPolyDP(c, 0.02 * peri, True)
      # area = cv2.contourArea(approx)
      if(len(approx) == 4):
        document = approx
        # break
    

    if(document is not None):
      cv2.drawContours(image, [document], -1, (0, 255, 0), 2)
      # return perspective.four_point_transform(image, document.reshape(4, 2))
      # cv2.resize(img, dim, interpolation = cv2.INTER_AREA)