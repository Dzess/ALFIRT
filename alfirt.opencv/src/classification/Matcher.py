'''
Created on 30-08-2011

@author: Ankhazam

Based on find_obj.py OpenCV2 sample
'''

import numpy as np
import cv2
from common import anorm

class Matcher(object):
    
    '''
    classdocs
    '''
    FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
    flann_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=4)

    def __init__(self, trainedObjects, imageWithObject):
        '''
        Constructor
        '''
        self.trainedObjects = trainedObjects
        self.image = imageWithObject

    
    def addTrainedObject(self, trainedObject):
        self.trainedObjects.append(trainedObject)        
    

    def match_bruteforce(self, desc1, desc2, r_threshold=0.75):
        res = []
        for i in xrange(len(desc1)):
            dist = anorm(desc2 - desc1[i])
            n1, n2 = dist.argsort()[:2]
            r = dist[n1] / dist[n2]
            if r < r_threshold:
                res.append((i, n1))
        return np.array(res)

    def match_flann(self, desc1, desc2, r_threshold=0.6):
        flann = cv2.flann_Index(desc2, self.flann_params)
        idx2, dist = flann.knnSearch(desc1, 2, params={}) # bug: need to provide empty dict
        mask = dist[:, 0] / dist[:, 1] < r_threshold
        idx1 = np.arange(len(desc1))
        pairs = np.int32(zip(idx1, idx2[:, 0]))
        return pairs[mask]

    def draw_match(self, img1, img2, p1, p2, status=None, H=None):
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1 + w2), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1 + w2] = img2
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
    
        if H is not None:
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = np.int32(cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0))
            cv2.polylines(vis, [corners], True, (255, 255, 255))
        
        if status is None:
            status = np.ones(len(p1), np.bool_)
        green = (0, 255, 0)
        red = (0, 0, 255)
        for (x1, y1), (x2, y2), inlier in zip(np.int32(p1), np.int32(p2), status):
            col = [red, green][inlier]
            if inlier:
                cv2.line(vis, (x1, y1), (x2 + w1, y2), col)
                cv2.circle(vis, (x1, y1), 2, col, -1)
                cv2.circle(vis, (x2 + w1, y2), 2, col, -1)
            else:
                r = 2
                thickness = 3
                cv2.line(vis, (x1 - r, y1 - r), (x1 + r, y1 + r), col, thickness)
                cv2.line(vis, (x1 - r, y1 + r), (x1 + r, y1 - r), col, thickness)
                cv2.line(vis, (x2 + w1 - r, y2 - r), (x2 + w1 + r, y2 + r), col, thickness)
                cv2.line(vis, (x2 + w1 - r, y2 + r), (x2 + w1 + r, y2 - r), col, thickness)
        return vis
    
    def matchObject(self, image, surfThreshold=400):
        '''
        @return: (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)
        '''
        surf = cv2.SURF(surfThreshold)
        kp, desc = surf.detect(image, None, False)
        desc.shape = (-1, surf.descriptorSize())
        
        # (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)
        bestMatchObject = (None, 0, None, None)
         
        # simple searching for best matched orientation        
        for trainedObject in self.trainedObjects:
            # might be useful to add return all the objects with their best orientation match
            ind = 0;
            for orientation in trainedObject.orientations:
                # we are using flannMatcher, can change to bruteForce'''
                matchResult = self.match_flann(orientation[2], desc)
                matched_p1 = np.array([orientation[1][i].pt for i, j in matchResult])
                matched_p2 = np.array([kp[j].pt for i, j in matchResult])
                H, status = cv2.findHomography(matched_p1, matched_p2, cv2.RANSAC, 5.0)
                #print '%d / %d  inliers/matched' % (np.sum(status), len(status))
                if len(status) > len(bestMatchObject[2]):
                    bestMatchObject = (trainedObject, ind, status, H)
                ind += 1
        return bestMatchObject
