import os
import cv2
from threading import Thread
# from capture_manager import CaptureManager
from window_manager import WindowManager
from filters.edge import canny, laplacian

from contours.detection import CircleDetector
from contours.detection import minimumarea
from contours.detection import bbox

from webcamvideostream import WebcamVideoStream
from remotepicamstream import RemotePiCamStream

from face.detector import FaceDetector
from contours.canny_edge_detector import CannyEdgeDetector

faces = FaceDetector()
circles = CircleDetector()
canny = CannyEdgeDetector()


detectors = [faces, circles, canny]
class Semblance(object):
    def __init__(self, source=0, directory="./tmp"):
        self._directory = directory
        self._windowManager = WindowManager('Semblance', self.onKeyPress)
        self.selection = 0
        if source == 0:
            self._stream = WebcamVideoStream(0).start()
        else:
            self._stream = RemotePiCamStream(source).start()

    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            frame = self._stream.read()
            if frame is not None:
                
                frame = canny.detect(frame)

                self._windowManager.show(frame)
            
            self._windowManager.processEvents()

    def onKeyPress(self, keycode):
        if keycode in (ord('q'), 27): # Quit/ESC
            self._windowManager.destroyWindow()
        # if keycode == ord("n"):
        #     self.toggle()

    def toggle(self):
        if self.selection == 0:
            self.selection = 1
        else:
            self.selection = 0




if __name__ == "__main__":
    Semblance(0).run()
