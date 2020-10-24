import os
import cv2
from capture_manager import CaptureManager
from window_manager import WindowManager
from filters.edge import canny, laplacian

from contours.detection import enclosingcircle
from contours.detection import minimumarea
from contours.detection import bbox


class Semblance(object):
    def __init__(self, directory="./tmp"):
        self._directory = directory
        self._windowManager = WindowManager('Semblance', self.onKeyPress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0), self._windowManager, True)

    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            if frame is not None:
                # edges = canny.apply(frame)
                # frame[edges > 100] = [255, 255, 255]

                # edges = laplacian.apply(frame)
                # cv2.merge(edges, frame)
                bbox(frame)
                pass

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeyPress(self, keycode):
        if keycode == 32:
            self._captureManager.writeImage(
                os.path.join(self._directory, 'screenshot.png'))
        elif keycode == 9:
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screencast.avi')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27:
            self._windowManager.destroyWindow()


if __name__ == "__main__":
    Semblance().run()
