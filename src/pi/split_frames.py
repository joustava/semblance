import io
import struct

class SplitFrames(object):
    """
    Splits a stream 
    """
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()

    def write(self, buffer):
        if buffer.startswith(b'\xff\xd8'):
            self.flush_frame()
       
        self.stream.write(buffer)
    
    def flush_frame(self):
        size = self.stream.tell()
        if size > 0:
            self.connection.write(struct.pack('<L', size))
            self.connection.flush()
            self.stream.seek(0)
            self.connection.write(self.stream.read(size))
            self.stream.seek(0)

