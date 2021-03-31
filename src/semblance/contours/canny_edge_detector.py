import cv2
import numpy as np

class CannyEdgeDetector:
    """
    The CannyEdgeDetector finds edges in an image and annotates them when requested.

    Similar but less clear detection can be applied with either Laplacian (see cv2.Laplacian) 
    or Sobel (see cv2.Sobel) method

    """
    def __init__(self, lower_threshold=30, upper_threshold=150):
      self._kernel = (5, 5)
      self._lower_threshold = lower_threshold
      self._upper_threshold = upper_threshold

    def detect(self, frame):
        """
        Detects edges in an image frame.

        Converts image to grayscale and applies blur (noise reduction) before running it through
        the Canny edge detection algorithm.    
        """
        
        _frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _frame = cv2.GaussianBlur(_frame, self._kernel, 0)
        _frame = cv2.Canny(_frame, self._lower_threshold, self._upper_threshold)
        _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2RGB)
        
        _frame *= np.array((1,1,1), np.uint8)
       
        return np.bitwise_or(_frame, frame)


