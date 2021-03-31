import io
import socket
import struct
import time
from picamera import PiCamera, Color
import datetime as dt
from fps import FPS
from split_frames import FrameGenerator

camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 30
camera.iso = 800
# camera.annotate_background = Color('blue')
# camera.annotate_text = "PiCam Client"
time.sleep(2)

gen = FrameGenerator()

try:
    fps = FPS().start()
    for _ in camera.capture_sequence(gen.frames(), 'jpeg', use_video_port=True):
        fps.update()

finally:
    fps.stop()
    gen.close()
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
