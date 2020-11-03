import io
import socket
import struct
import time
from picamera import PiCamera
from fps import FPS

# # scp -r src/picamexample/client.py pi@raspberrypi.local:/home/pi/client.py
# # basic version [INFO] approx. FPS: 16.09 meaning that this version can process max 16 frames a second at 640/480
# # A queue implementation is extremely slow as linux has speed limitation of pipe implemetation (we are handling image data)

# imagezmq and no queue for frames gives about 18frames/sec


# This version reports around 29fps.

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.2.108', 8000))
connection = client_socket.makefile('wb')

try:
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        time.sleep(2)
        start = time.time()
        stream = io.BytesIO()
        # Use the video-port for captures...

        fps = FPS().start()
        for frame in camera.capture_continuous(stream, 'jpeg',
                                               use_video_port=True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            if time.time() - start > 30:
                break
            stream.seek(0)
            stream.truncate()
            fps.update()

        fps.stop()
        connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    client_socket.close()
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
