import cv2
import numpy as np
from features.edgedetection.canny_edge_filter import CannyEdgeFilter
class CannyEdgeDetector:
    """
    The CannyEdgeDetector finds edges in an image and visulaizes them on the original image.

    Similar but less clear detection can be applied with either Laplacian (see cv2.Laplacian) 
    or Sobel (see cv2.Sobel) method
    """
    def __init__(self):
      self.filter = CannyEdgeFilter()


    def detect(self, frame):
        """
        Detects edges in an image frame.

        Converts image to grayscale and applies blur (noise reduction) before running it through
        the Canny edge detection algorithm.    
        """
        _frame = self.filter.apply(frame)

        _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2RGB)
        _frame *= np.array((1,1,1), np.uint8)
        _frame = np.bitwise_or(_frame, frame)
        
        return _frame