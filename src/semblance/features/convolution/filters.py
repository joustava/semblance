import numpy
from features.convolution.base import ConvolutionFilter


class SharpenFilter(ConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])
        ConvolutionFilter.__init__(self, kernel)


class SobelXFilter(ConvolutionFilter):
    """
    Takes the gradient in the x direction.
    This emphasizes edges closer to vertical.

    Works best on a single color channel

    Example:
    >>> gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    """

    def __init__(self):
        kernel = numpy.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ])
        ConvolutionFilter.__init__(self, kernel)


class SobelYFilter(ConvolutionFilter):
    """
    Takes the gradient in the y direction.
    This emphasizes edges closer to horizontal.

    Works best on a single color channel

    Example:
    >>> gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    """

    def __init__(self):
        kernel = numpy.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ])
        ConvolutionFilter.__init__(self, kernel)


class EdgesFilter(ConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ])
        ConvolutionFilter.__init__(self, kernel)


class BlurFilter(ConvolutionFilter):
    def __init__(self):
        kernel = np.full((5, 5), 0.04, dtype=float)
        ConvolutionFilter.__init__(self, kernel)


class EmbossFilter(ConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([
            [-2, -1, 0],
            [-1,  1, 1],
            [0,  1, 2]
        ])
        ConvolutionFilter.__init__(self, kernel)
