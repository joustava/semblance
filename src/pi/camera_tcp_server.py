import io
import socket
import time
import struct
from picamera import PiCamera, Color
from fps import FPS
from split_frames import SplitFrames

camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 30
camera.annotate_background = Color('blue')
camera.annotate_text = "PiCam Server"
time.sleep(2)

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')

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


try:
    output = SplitFrames(connection)
    fps = FPS().start()
    for _ in camera.capture_sequence(frame_sequence(), format='jpeg'):
      fps.update()


finally:
  fps.stop()
  connection.write(struct.pack('<L', 0))
  connection.close()
  server_socket.close()
  print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
