import io
import socket
import struct
import cv2
import numpy as np

# Server config
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')

try:
    while True:
        image_len = struct.unpack(
            '<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)

        # frame = np.fromfile(image_stream, dtype=np.uint8)

        frame = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), 1)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    connection.close()
    server_socket.close()

# from imutils import build_montages
# from datetime import datetime
# import numpy as np
# import imagezmq
# import imutils
# import cv2

# imageHub = imagezmq.ImageHub(open_port='tcp://*:5555')
# # imageHub.zmqsocket.setsockopt("ZMQ_REQ_RELAXED", b'1')
# # imageHub.zmqsocket.setsockopt("ZMQ_REQ_CORRELATE", b'1')

# while True:
#     (client, frame) = imageHub.recv_image()
#     imageHub.send_reply(b'OK')

#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
