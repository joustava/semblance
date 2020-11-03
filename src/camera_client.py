import imagezmq as mq
from imutils.video import VideoStream
import datetime
import sys
import io
import socket
import struct
import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
from queue import Queue


class PiVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32, **kwargs):
        # initialize the camera
        self.camera = PiCamera()

        # set camera parameters
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        # set optional camera parameters (refer to PiCamera docs)
        for (arg, value) in kwargs.items():
            setattr(self.camera, arg, value)

        # initialize the stream
        self.rawCapture = io.BytesIO()  # PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, 'jpeg',
                                                     use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frames = Queue(maxsize=128)
        # self.frame = None
        self.stopped = False
        self.data = (None, 0)

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        # t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for _frame in self.stream:
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                break

            if not self.frames.full():
                # get frame size
                size = self.rawCapture.tell()
                # rewind and get frame
                self.rawCapture.seek(0)

                frame = self.rawCapture.read()
                # size = len(frame)
                # reset the stream for next capture
                self.rawCapture.seek(0)
                self.rawCapture.truncate()

                if size == 0:
                    self.stop()
                    return
                # add the frame to the queue
                #self.frames.put((frame, size))
                self.data = (frame, size)

    def read(self):
        # return the frame most recently read
        # return self.frames.get()
        return self.data

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1
        # self._end = datetime.datetime.now()

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()

# # scp -r src/picamexample/client.py pi@raspberrypi.local:/home/pi/client.py
# # basic version [INFO] approx. FPS: 16.09 meaning that this version can process max 16 frames a second at 640/480
# # A queue implementation is extremely slow as linux has speed limitation of pipe implemetation (we are handling image data)


# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('192.168.2.108', 8000))
# connection = client_socket.makefile('wb')
# try:
#     vs = PiVideoStream(resolution=(640, 480), framerate=32).start()
#     time.sleep(1.0)
#     start = time.time()
#     fps = FPS().start()
#     while True:
#         frame, size = vs.read()
#         connection.write(struct.pack('<L', size))
#         connection.write(frame)
#         connection.flush()
#         fps.update()
#         if time.time() - start > 30:
#             break

#     # with picamera.PiCamera() as camera:
#     #     camera.resolution = (640, 480)
#     #     camera.framerate = 30
#     #     time.sleep(2)
#     #     start = time.time()
#     #     stream = io.BytesIO()
#     #     # Use the video-port for captures...

#     #     stream = camera.capture_continuous(stream, 'jpeg',
#     #                                        use_video_port=True)

#     #     fps = FPS().start()
#     #     for frame in stream:
#     #         connection.write(struct.pack('<L', stream.tell()))
#     #         connection.flush()
#     #         stream.seek(0)
#     #         connection.write(stream.read())
#     #         if time.time() - start > 30:
#     #             break
#     #         stream.seek(0)
#     #         stream.truncate()
#     #         fps.update()

#     fps.stop()
#     connection.write(struct.pack('<L', 0))
# finally:
#     connection.close()
#     client_socket.close()
#     print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# # From https://github.com/jrosebr1/imutils


# zmq version

sender = mq.ImageSender(connect_to="tcp://192.168.2.108:5555")

host = socket.gethostname()
# The camera is capable of:
#   2592 x 1944 pixel static images and for video
#   1080p @ 30fps (Full HD 1920×1080)
#   720p @ 60fps (HD Ready 1280×720)
#   640x480p 60/90
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
