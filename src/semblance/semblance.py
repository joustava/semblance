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
from features.facedetection.facial_landmark_detector import FacialLandmarkDetector
from features.facedetection.eye_blink_detector import EyeBlinkDetector
from features.edgedetection.canny_edge_detector import CannyEdgeDetector
from features.documentscanner.pdf_scanner import PDFScanner
from features.tracking.tennis_ball_detector import TennisBallDetector
from features.measure.test import SizeDetector

faces = FaceDetector()
facial = FacialLandmarkDetector()
# emboss = EmbossFilter()
canny = CannyEdgeDetector()
scanner = PDFScanner()
tracker = TennisBallDetector()
measure = SizeDetector()
eyeblink = EyeBlinkDetector()
detectors = [
    (measure, "Measures"),
    (scanner, "Doc Scan"), 
    (canny, "Canny Edges"),
    (faces, "Face Detection"),
    (facial, "Facial Landmark Detection"),
    (tracker, "Ball Tracker"),
    (eyeblink, "Eye Blink")
]

class Semblance(object):
    def __init__(self, port=0, directory="./tmp"):
        signal.signal(signal.SIGINT, self._handle_signal)
        self._directory = directory
        self._windowManager = WindowManager('Semblance', self._onKeyPress)
        self._selection = 0
        self._overlay = False
        self._mirror = False
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
                # if(self._mirror):
                #     frame = np.fliplr(frame)
                    
                feature = detectors[self._selection]
                _frame = feature[0].detect(frame)
                
                _frame = self.add_label(_frame, feature[1])
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
        if keycode == ord("m"):
            self._mirror = not self._mirror

    def snapshot(self, frame):
        path = "~/Downloads/snapshot_" + dt.datetime.today().isoformat() + ".jpg"
        path = os.path.expanduser(path)
        cv2.imwrite(path, frame)

    def add_label(self, frame, text):
        (h, w) = frame.shape[:2]

        
        cv2.putText(frame, text, (20, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        
        return frame
    
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
