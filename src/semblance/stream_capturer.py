from threading import Thread
import sys
import io
import cv2
from queue import Queue


class StreamCapture(object):
    def __init__(self, frames=64):
        """

        :frames: integer setting the size of the frame queue, byt default it gives about 2 seconds buffer around 30 frame/s
        """
        self.stream = io.BytesIO()
        self.stopped = False
        self.frames = Queue(maxsize=frames)

    def start(self):
        """
        Start a thread that grabs frames from a stream in a non-blocking way. 
        """
        runner = Thread(target=self.grab, args=())
        runner.daemon = True
        runner.start()
        return self

    def stop(self):
        """
        Flag the thread to stop execution
        """
        self.stopped = True

    def retrieve(self, frame, channel):
        """
        The method decodes and returns the just grabbed frame
        """
        return self.frames.get()

    def grab(self):
        """
        Grab next frame in stream
        """
        while True:
            if self.stopped:
                return

            if not self.frames.full():
                (grabbed, frame) = self.stream.read()
                if not grabbed:
                    self.stop()
                    return
                # add the frame to the queue
                self.frames.put(frame)

    def get(self, key):
        """
        Get meta data from frame or stream.

        Supports cv2.CAP_PROP_FPS, cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT
        """
        pass
