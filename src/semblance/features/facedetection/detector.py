import cv2
import imutils
import numpy as np

class FaceDetector:
  """
  This detector uses a pre-trained Caffe model to detect faces in images and draws bounding boxes
  for those detections that exceed the configured min confidence score.
  """
  def __init__(self, confidence=0.5):
    self._net = cv2.dnn.readNetFromCaffe("src/semblance/features/facedetection/deploy.prototxt", "src/semblance/features/facedetection/res10_300x300_ssd_iter_140000.caffemodel")
    self._confidence = confidence

  def detect(self, frame):
    # frame = imutils.resize(image, width=400)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    self._net.setInput(blob)
    detections = self._net.forward()

    for i in range(0, detections.shape[2]):
      # extract the confidence (i.e., probability) associated with the
      # prediction
      confidence = detections[0, 0, i, 2]
      # filter out weak detections by ensuring the `confidence` is
      # greater than the minimum confidence
      if confidence < self._confidence:
        continue
      # compute the (x, y)-coordinates of the bounding box for the
      # object
      box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
      (startX, startY, endX, endY) = box.astype("int")
  
      # draw the bounding box of the face along with the associated
      # probability
      text = "{:.2f}%".format(confidence * 100)
      y = startY - 10 if startY - 10 > 10 else startY + 10
      cv2.rectangle(frame, (startX, startY), (endX, endY),
        (0, 0, 255), 2)
      cv2.putText(frame, text, (startX, y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    
    return frame