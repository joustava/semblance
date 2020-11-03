from imagezmq import ImageSender
from pi_camera_capture import PiVideoStream
import time
import socket
from fps import FPS

sender = ImageSender(connect_to="tcp://192.168.2.108:5555")

host = socket.gethostname()
# The camera is capable of:
#   2592 x 1944 pixel static images and for video
#   1080p @ 30fps (Full HD 1920×1080)
#   720p @ 60fps (HD Ready 1280×720)
#   640x480p 60/90
#
# This reports a fps of about [INFO] approx. FPS: 22.64

stream = PiVideoStream(resolution=(640, 480), framerate=32).start()
time.sleep(2)
start = time.time()
fps = FPS().start()
while True:
    frame, size = stream.read()
    sender.send_jpg(host, frame)
    fps.update()
    if time.time() - start > 30:
        fps.stop()
        break

print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
