import os
import sys
import signal
from threading import Thread
import datetime as dt
import cv2
import numpy as np
import argparse
# from capture_manager import CaptureManager
from window_manager import WindowManager

from webcamvideostream import WebcamVideoStream
from remotepicamstream import RemotePiCamStream

from features.convolution.filters import EmbossFilter

from features.facedetection.detector import FaceDetector
from features.edgedetection.canny_edge_detector import CannyEdgeDetector
from features.documentscanner.pdf_scanner import PDFScanner
from features.tracking.tennis_ball_detector import TennisBallDetector
from features.measure.test import SizeDetector

faces = FaceDetector()
# emboss = EmbossFilter()
canny = CannyEdgeDetector()
scanner = PDFScanner()
tracker = TennisBallDetector()
measure = SizeDetector()
detectors = [measure, scanner, canny, faces, tracker]

class Semblance(object):
    def __init__(self, port=0, directory="./tmp"):
        signal.signal(signal.SIGINT, self._handle_signal)
        self._directory = directory
        self._windowManager = WindowManager('Semblance', self._onKeyPress)
        self._selection = 0
        self._overlay = False
        self._take = False
        if port == 0:
            self._stream = WebcamVideoStream(0).start()
        else:
            self._stream = RemotePiCamStream().start()

    def run(self):
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            frame = self._stream.read()
            if frame is not None:
                
                _frame = detectors[self._selection].detect(frame)
                
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-pi', '--picamera', required=False, help='Use remote RPI camera', action='store_true')

    args = vars(parser.parse_args())

    if args['picamera']:
        Semblance(8000).run()
    else:
        Semblance(0).run()
