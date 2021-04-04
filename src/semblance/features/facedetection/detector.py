import cv2
import imutils
import numpy as np
from features.tracking.centroid_tracker import CentroidTracker
class FaceDetector:
  """
  This detector uses a pre-trained Caffe model to detect faces in images and draws bounding boxes
  for those detections that exceed the configured min confidence score.
  """
  def __init__(self, confidence=0.5):
    self._net = cv2.dnn.readNetFromCaffe("src/semblance/features/facedetection/deploy.prototxt", "src/semblance/features/facedetection/res10_300x300_ssd_iter_140000.caffemodel")
    self._min_confidence = confidence
    self._tracker = CentroidTracker()

  def visualize(self, frame, detections):
    (H, W) = frame.shape[:2]
    rects = []
    for i in range(0, detections.shape[2]):
        # filter out weak detections by ensuring the predicted
        # probability is greater than a minimum threshold
        confidence = detections[0, 0, i, 2]
        if confidence > self._min_confidence:
            # compute the (x, y)-coordinates of the bounding box for
            # the object, then update the bounding box rectangles list
            box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            rects.append(box.astype("int"))
            # draw a bounding box surrounding the object so we can
            # visualize it
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    
    return frame, rects
  
  def track(self, frame, rects):
    # update our centroid tracker using the computed set of bounding
    # box rectangles
    objects = self._tracker.update(rects)
    # loop over the tracked objects
    for (objectID, centroid) in objects.items():
        # draw both the ID of the object and the centroid of the
        # object on the output frame
        text = "ID {}".format(objectID)
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
    
    return frame

  def detect(self, frame):
    # frame = imutils.resize(image, width=400)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    self._net.setInput(blob)
    detections = self._net.forward()

    frame, rects = self.visualize(frame, detections)
    self.track(frame, rects)

    return frame