'''
Created on 30-08-2011

@author: Ankhazam

Based on find_obj.py OpenCV2 sample
'''

import numpy as np
import cv2
from common import anorm

class FlannMatcher(object):
    '''
    Main recognition and training module.
    '''
    
    FLANN_INDEX_KDTREE = 1  # OpenCV bug: flann enums are missing
    flann_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=4)

    def __init__(self, trainedObjects, imageWithObject, surfThreshold=400):
        '''
        Constructor
        
        @param trainedObjects: List of @see: TrainedObject used as recognition DB
        @param imageWithObject: Image containing one of the learnt objects.
        @param surfThreshold:  Threshold that was used to train the objects (if equal for all)
        '''
        self.trainedObjects = trainedObjects
        self.image = imageWithObject
        self.surfThreshold = surfThreshold
        self.surf = cv2.SURF(self.surfThreshold)

    
    def addTrainedObject(self, trainedObject):
        '''
        Extends the loaded database with a new @see: TrainedObject
        '''
        self.trainedObjects.append(trainedObject)        
    

    def matchUsingBruteforce(self, desc1, desc2, r_threshold=0.75):
        res = []
        for i in xrange(len(desc1)):
            dist = anorm(desc2 - desc1[i])
            n1, n2 = dist.argsort()[:2]
            r = dist[n1] / dist[n2]
            if r < r_threshold:
                res.append((i, n1))
        return np.array(res)
    

    def matchUsingFlann(self, desc1, desc2, r_threshold=0.6):
        '''
        Internal flann descriptors matcher in order to find the best match.
        
        @param desc1, desc2: SURF features descriptors of currently processed object orientation and the test image.
        @param r_threshold: Tunnable threshold for kNN normalized distance inside the descriptors space.
        '''
        flann = cv2.flann_Index(desc2, self.flann_params)
        idx2, dist = flann.knnSearch(desc1, 2, params={}) # bug: need to provide empty dict
        mask = dist[:, 0] / dist[:, 1] < r_threshold
        idx1 = np.arange(len(desc1))
        pairs = np.int32(zip(idx1, idx2[:, 0]))
        return pairs[mask]
    
    
    def matchWithGivenflann(self, desc1, flannIndex, r_threshold=0.6):
        '''
        Internal flann descriptors matcher in order to find the best match.
        
        @param desc1: SURF features descriptors of currently processed object orientation and the test image.
        @param flannIndex: PreGenerated FlannIndex to be used for searching 
        @param r_threshold: Tunnable threshold for kNN normalized distance inside the descriptors space.
        
        @return: Array of matched points.
        '''
        idx2, dist = flannIndex.knnSearch(desc1, 2, params={}) # bug: need to provide empty dict
        mask = dist[:, 0] / dist[:, 1] < r_threshold
        idx1 = np.arange(len(desc1))
        pairs = np.int32(zip(idx1, idx2[:, 0]))
        return pairs[mask]

        
    def draw_match(self, img1, img2, p1, p2, status=None, H=None):
        '''
        Allows visualization of a match by drawing lines between points on object and test image.
        Also presents the recognized plane using RANSAC method.
        
        @param img1: Image of the recognized object used for training.
        @param img2: Image containing the recognized object somewhere on its' scene.
        @param p1: Matched points found on trained image.
        @param p2: Matched points on the test image.
        @param status: outputMask from @see cv2.findHomography()
        @param H: the Homography matrix from @see cv2.findHomography()
        
        @return: Image of the match.    
        '''
        
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
    
    
    def matchObject(self, image, surfThreshold=None):
        '''
        Finds best match for each object in the database.
        
        @param image: Image with object(s) to be found.
        @param surfThreshold: Threshold for Hessian detector in SURF method used for training the objects.
        This method adapts however this threshold automatically basing on the read from each TrainedObject.
          
        @return: List of tuples (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)
        '''
        # create new surf extractor only if needed
        if (surfThreshold is not None) and (surfThreshold != self.surfThreshold):
            self.surfThreshold = surfThreshold
            self.surf = cv2.SURF(self.surfThreshold)
            
        kp, desc = self.surf.detect(image, None, False)
        desc.shape = (-1, self.surf.descriptorSize())
        flannIndex = cv2.flann_Index(desc, self.flann_params)
        
        # list of (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)        
        bestMatches = None
        
        # simple searching for best matched orientation        
        for trainedObject in self.trainedObjects:

            # we need to recreate the flann index if objects are trained with different thresholds
            if (trainedObject.surfThreshold != self.surfThreshold) :
                self.surfThreshold = trainedObject.surfThreshold
                self.surf = cv2.SURF(self.surfThreshold)
            
                kp, desc = self.surf.detect(image, None, False)
                desc.shape = (-1, self.surf.descriptorSize())
                flannIndex = cv2.flann_Index(desc, self.flann_params)
                 
            # (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)
            bestMatchObject = (None, 0, None, None)
            ind = 0
                        
            for orientation in trainedObject.orientations:
                # we are using flannMatcher, can change to bruteForce'''
                matchResult = self.matchWithGivenflann(orientation[2], flannIndex) # optimized with preGenerated FlannIndex
                matched_p1 = np.array([orientation[1][i].pt for i, j in matchResult])
                matched_p2 = np.array([kp[j].pt for i, j in matchResult])
                H, status = cv2.findHomography(matched_p1, matched_p2, cv2.RANSAC, 5.0)
                #print '%d / %d  inliers/matched' % (np.sum(status), len(status))
                if len(status) > len(bestMatchObject[2]):
                    bestMatchObject = (trainedObject, ind, status, H)
                ind += 1
                
            # appends to the results the best match for each TrainedObject
            bestMatches.append(bestMatchObject)
            
        return bestMatches

