import uuid
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class CentroidTracker:
    def __init__(self, trackingThreshold=64):
        self.trackedObjects = OrderedDict()
        self.disappearedObjects = OrderedDict()
        self.trackingThreshold = trackingThreshold

        self.nextObjectUUID = 0 #uuid.uuid4()

    def register(self, centroid):
        self.trackedObjects[self.nextObjectUUID] = centroid
        self.disappearedObjects[self.nextObjectUUID] = 0
        self.nextObjectUUID += 1 #uuid.uuid4()
      
    def deregister(self, objectUUID):
        del self.trackedObjects[objectUUID]
        del self.disappearedObjects[objectUUID]

    def update(self, rects):
        if len(rects) == 0:
            for objectUUID in list(self.disappearedObjects.keys()):
                self.disappearedObjects[objectUUID] += 1
                if self.disappearedObjects[objectUUID] > self.trackingThreshold:
                    self.deregister(objectUUID)
              
            return self.trackedObjects
          
        inputCentroids = np.zeros((len(rects), 2), dtype="int")
          
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)


            if len(self.trackedObjects) == 0:
                for i in range(0, len(inputCentroids)):
                    self.register(inputCentroids[i])
            else:
                objectIDs = list(self.trackedObjects.keys())
                objectCentroids = list(self.trackedObjects.values())
                
                D = dist.cdist(np.array(objectCentroids), inputCentroids)
                
                rows = D.min(axis=1).argsort()
                cols = D.argmin(axis=1)[rows]

                
                usedRows = set()
                usedCols = set()
                
                for (row, col) in zip(rows, cols):
                    
                    if row in usedRows or col in usedCols:
                        continue
                    
                    objectID = objectIDs[row]
                    self.trackedObjects[objectID] = inputCentroids[col]
                    self.disappearedObjects[objectID] = 0
                   
                    usedRows.add(row)
                    usedCols.add(col)

                    unusedRows = set(range(0, D.shape[0])).difference(usedRows)
                    unusedCols = set(range(0, D.shape[1])).difference(usedCols)

                    if D.shape[0] >= D.shape[1]:
                        for row in unusedRows:
                            objectID = objectIDs[row]
                            self.disappearedObjects[objectID] += 1
                            if self.disappearedObjects[objectID] > self.trackingThreshold:
                                self.deregister(objectID)
                    else:
                        for col in unusedCols:
                            self.register(inputCentroids[col])

        return self.trackedObjects