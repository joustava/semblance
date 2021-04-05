import io
import os
import cv2
import struct
import socket
import numpy as np
from threading import Thread


class RemotePiCamStream:
    def __init__(self, src=8000, name="RemotePicamVideoStream"):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(('0.0.0.0', src))
        self._socket.listen(0)
        self._conn = self._socket.accept()[0].makefile('rb')
        
        self._image_stream = None
        self._frame = self._next_frame()
        
        self.name = name
        self.stopped = False

    def start(self):
        """ Start a thread to read frames from the video stream. """
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self
        

    def update(self):
        """ Continuously capture the latest frame. """
        while True:
            if self.stopped:
                return

            self._next_frame()


    def read(self):
        """ Get the latest decoded frame from the stream. """
        return cv2.imdecode(np.frombuffer(self._frame, np.uint8), 1)


    def stop(self):
        """ Stop streaming, cleanup/close resources. """
        self._conn.close()
        self._socket.close()
        self.stopped = True


    def _next_frame(self):
        """ Get the next frame from the mjpeg stream. """
        image_len = struct.unpack('<L', self._conn.read(struct.calcsize('<L')))[0]
        if not image_len:
            return

        self._image_stream = io.BytesIO()
        self._image_stream.write(self._conn.read(image_len))
        self._image_stream.seek(0)
        self._frame = self._image_stream.read()


    def is_socket_closed(self, sock: socket.socket) -> bool:
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            logger.exception("unexpected exception when checking if a socket is closed")
            return False
        return False