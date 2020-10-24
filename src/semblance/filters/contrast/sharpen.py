import numpy
from base.convolution import ConvolutionFilter


class SharpenFilter(ConvolutionFilter):
    def __init__(self):
        kernel = numpy.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
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
