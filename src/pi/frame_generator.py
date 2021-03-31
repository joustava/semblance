import io
import struct
import socket

class FrameGenerator(object):
    """
    Splits a stream in frames and puts these onto a tcp socket. 
    """
    def __init__(self, address='192.168.2.107', port=8000):
        """
        Creates a new FrameGenerator that connect to tcp://addres:port
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((address, port))
        self._conn = self._socket.makefile('wb')

    def close(self):
      self._conn.write(struct.pack('<L', 0))
      self._conn.close()
      self._socket.close()
      
    def frames(self):
        stream = io.BytesIO()
        while True:
            yield stream
            self._conn.write(struct.pack('<L', stream.tell()))
            self._conn.flush()
            stream.seek(0)
            self._conn.write(stream.read())
            stream.seek(0)
            stream.truncate()

