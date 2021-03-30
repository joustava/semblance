import os
import cv2
from threading import Thread
# from capture_manager import CaptureManager
from window_manager import WindowManager
from filters.edge import canny, laplacian

from contours.detection import enclosingcircle
from contours.detection import minimumarea
from contours.detection import bbox

from webcamvideostream import WebcamVideoStream
from remotepicamstream import RemotePiCamStream

class Semblance(object):
    def __init__(self, source=0, directory="./tmp"):
        self._directory = directory
        self._windowManager = WindowManager('Semblance', self.onKeyPress)
        if source == 0:
            self._stream = WebcamVideoStream(0).start()
        else:
            self._stream = RemotePiCamStream(source).start()

    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            frame = self._stream.read()
            if frame is not None:
                bbox(frame)
                frame = cv2.putText(frame, "rpi", (50, 50), cv2.FONT_ITALIC, 
                   1, (255, 0, 0), 1, cv2.LINE_AA)

                self._windowManager.show(frame)
            
            self._windowManager.processEvents()

    def onKeyPress(self, keycode):
        if keycode == 27: # ESC
            self._windowManager.destroyWindow()


if __name__ == "__main__":
    Semblance(8000).run()
