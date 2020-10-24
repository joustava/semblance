import cv2
import numpy


def apply(image, k=7, edge=5):
    """
    Applies Laplacian Edge detection.

    Example:
    >>>
    >>>

    :param image: The source image.
    :param sigma: Controls the threshold range, low sigma smaller range and larger sigma larger range.
    :param k:     Guassian blur kernel size, must be odd integer 
    :return: detected Canny Edges.
    """
    blur = cv2.medianBlur(image, k)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(gray, cv2.CV_8U, gray, ksize=edge)
    normalizedInverseAlpha = (1.0/255) * (255 * gray)
    channels = cv2.split(image)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha

    return channels
