import numpy as np
import imagezmq
import imutils
import cv2

imageHub = imagezmq.ImageHub(open_port='tcp://*:5555')
# imageHub.zmqsocket.setsockopt("ZMQ_REQ_RELAXED", b'1')
# imageHub.zmqsocket.setsockopt("ZMQ_REQ_CORRELATE", b'1')

while True:
    (client, frame) = imageHub.recv_jpg()
    imageHub.send_reply(b'OK')

    frame = cv2.imdecode(np.frombuffer(frame, np.uint8), 1)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
