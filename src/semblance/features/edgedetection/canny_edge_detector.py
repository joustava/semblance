import cv2
import numpy as np
from features.edgedetection.canny_edge_filter import CannyEdgeFilter
class CannyEdgeDetector:
    """
    The CannyEdgeDetector finds edges in an image and visualizes them on the original image.

    Similar but less clear detection can be applied with either Laplacian (see cv2.Laplacian) 
    or Sobel (see cv2.Sobel) method
    """
    def __init__(self):
      self.canny_edge_filter = CannyEdgeFilter()


    def detect(self, frame):
        """
        Detects edges in an image frame.
        """
        _frame = self.canny_edge_filter.apply(frame)

        _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2RGB)
        _frame *= np.array((1,1,1), np.uint8)
        _frame = np.bitwise_or(_frame, frame)
        
        return _frame