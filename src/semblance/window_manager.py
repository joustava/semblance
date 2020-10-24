import cv2


class WindowManager(object):
    def __init__(self, windowName, keyPressCallback):
        self.keyPressCallback = keyPressCallback
        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self.isWindowCreated = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keyPressCallback is not None and keycode != -1:
            self.keyPressCallback(keycode)
