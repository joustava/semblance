import io
import socket
import struct
import time
from picamera import PiCamera, Color
import datetime as dt
from fps import FPS
from split_frames import SplitFrames

camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 30
camera.iso = 800
# camera.annotate_background = Color('blue')
# camera.annotate_text = "PiCam Client"
time.sleep(2)

def frame_sequence():
    stream = io.BytesIO()
    while True:
        yield stream
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        stream.seek(0)
        stream.truncate()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.2.107', 8000))
connection = client_socket.makefile('wb')

try:
    # output = SplitFrames(connection)
   
    fps = FPS().start()
    for _ in camera.capture_sequence(frame_sequence(), 'jpeg', use_video_port=True):
        fps.update()

finally:
    fps.stop()
    connection.write(struct.pack('<L', 0))
    connection.close()
    client_socket.close()
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
