import cv2
import numpy


def apply(image, sigma=0.4, k=3):
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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (k, k), 0, dst=None,
                            sigmaY=None, borderType=None)
    v = numpy.median(blur)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    return cv2.Canny(blur, lower, upper)
