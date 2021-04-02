import os
import sys
import signal
from threading import Thread
import datetime as dt
import cv2
import numpy as np
# from capture_manager import CaptureManager
from window_manager import WindowManager

from webcamvideostream import WebcamVideoStream
from remotepicamstream import RemotePiCamStream

from features.convolution.filters import EmbossFilter

from features.facedetection.detector import FaceDetector
from features.edgedetection.canny_edge_detector import CannyEdgeDetector
from features.documentscanner.pdf_scanner import PDFScanner

faces = FaceDetector()
# emboss = EmbossFilter()
canny = CannyEdgeDetector()
scanner = PDFScanner()

detectors = [scanner, canny, faces]

class Semblance(object):
    def __init__(self, source=0, directory="./tmp"):
        signal.signal(signal.SIGINT, self._handle_signal)
        self._directory = directory
        self._windowManager = WindowManager('Semblance', self._onKeyPress)
        self._selection = 0
        self._overlay = False
        self._take = False
        if source == 0:
            self._stream = WebcamVideoStream(0).start()
        else:
            self._stream = RemotePiCamStream(source).start()

    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            frame = self._stream.read()
            if frame is not None:
                
                _frame = detectors[self._selection].detect(frame)
                
                # if(self._overlay):
                #     _frame = np.bitwise_or(_frame, frame)
                
                
                self._windowManager.show(_frame)
                if(self._take):
                    self.snapshot(_frame)
                    self._take = False
            
            self._windowManager.processEvents()

    def _onKeyPress(self, keycode):
        if keycode in (ord('q'), 27): # Quit/ESC
            self._windowManager.destroyWindow()
        if keycode == ord("s"):
            self._take = True
        if keycode == ord("d"):
            self._cycle_choice()
        if keycode == ord("o"):
            self._overlay = not self._overlay

    def snapshot(self, frame):
        path = "~/Downloads/snapshot_" + dt.datetime.today().isoformat() + ".jpg"
        path = os.path.expanduser(path)
        cv2.imwrite(path, frame)

    def _cycle_choice(self):
        if(self._selection < len(detectors) - 1):
            self._selection += 1
        else:
            self._selection = 0

    def _handle_signal(self, signal, frame):
        print('Exiting Semblance, ciao!')
        self._windowManager.destroyWindow()
        sys.exit(0)


if __name__ == "__main__":
    Semblance(8000).run()
