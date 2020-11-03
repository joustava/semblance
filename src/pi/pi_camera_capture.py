import io
from threading import Thread
from picamera import PiCamera


class PiVideoStream:
    """
    For use on Raspberry Pi with Pi Camera (v1.3) only
    """

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
        # NOT queu like this is horribly slow for image data
        # self.frames = Queue(maxsize=128)
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
            # self.frames.put((frame, size))
            self.data = (frame, size)

    def read(self):
        # return the frame most recently read
        # return self.frames.get()
        return self.data

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
