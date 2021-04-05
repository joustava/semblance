import io
import struct
import socket

class FrameGenerator(object):
    """
    Splits a stream in frames and their sizes and puts these on the output.
    """
    def __init__(self, output):
        """
        Creates a new FrameGenerator with output as the destination of the stream
        """
        self.output = output
      
    def frames(self):
        stream = io.BytesIO()
        while True:
            yield stream
            self.output.write(struct.pack('<L', stream.tell()))
            self.output.flush()
            stream.seek(0)
            self.output.write(stream.read())
            stream.seek(0)
            stream.truncate()