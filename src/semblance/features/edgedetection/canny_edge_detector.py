import cv2
import numpy as np

class CannyEdgeDetector:
    """
    The CannyEdgeDetector finds edges in an image and annotates them when requested.

    Similar but less clear detection can be applied with either Laplacian (see cv2.Laplacian) 
    or Sobel (see cv2.Sobel) method

    """
    def __init__(self, k=5, lower_threshold=30, upper_threshold=150, auto=True):
      self._kernel = (k, k)
      self._lower_threshold = lower_threshold
      self._upper_threshold = upper_threshold
      self._auto = auto

    def detect(self, frame):
        """
        Detects edges in an image frame.

        Converts image to grayscale and applies blur (noise reduction) before running it through
        the Canny edge detection algorithm.    
        """
        
        
        if(self._auto):
          _frame = self._auto_detect(frame)
        else:
          _frame = self._manu_detect(frame)

        _frame = cv2.cvtColor(_frame, cv2.COLOR_GRAY2RGB)
        _frame *= np.array((1,1,1), np.uint8)
       
        return _frame

    def _manu_detect(self, frame):
        grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayed, self._kernel, 0, dst=None, sigmaY=None, borderType=None)
        return cv2.Canny(blurred, self._lower_threshold, self._upper_threshold)
        
    def _auto_detect(self, frame, sigma=0.4):
      """
      Applies the Canny Edge detection by setting the upper and lower bounds based
      on the median value of pixel intensity in the whole image.

      Example:
      >>> edges = canny.apply(frame)
      >>> frame[edges > 100] = [255, 255, 255]

      :param image: The source image.
      :param sigma: Controls the threshold range, low sigma smaller range and larger sigma larger range.
      :param k:     Guassian blur kernel size, must be odd integer 
      :return: detected Canny Edges.
      """
      grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(grayed, self._kernel, 0, dst=None, sigmaY=None, borderType=None)
      v = np.median(blurred)
      lower = int(max(0, (1.0 - sigma) * v))
      upper = int(min(255, (1.0 + sigma) * v))
      return cv2.Canny(blurred, lower, upper)

    
