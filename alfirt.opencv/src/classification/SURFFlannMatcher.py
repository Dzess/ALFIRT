'''
Created on 30-08-2011

@author: Ankhazam

Based on find_obj.py OpenCV2 sample
'''

import numpy as np
import cv2
from common import anorm

class SURFFlannMatcher(object):
    '''
    Main recognition and training module.
    '''

    FLANN_INDEX_KDTREE = 1  # OpenCV bug: flann enums are missing
    flann_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=4)

    def __init__(self, trainedObjects, surfThreshold=400):
        '''
        Constructor
        
        @param trainedObjects: List of @see: TrainedObject used as recognition DB
        @param surfThreshold:  Threshold that was used to train the objects (if equal for all)
        '''
        self.trainedObjects = trainedObjects
        self.surfThreshold = surfThreshold
        self.surf = cv2.SURF(self.surfThreshold)


    def addTrainedObject(self, trainedObject):
        '''
        Extends the loaded database with a new @see: TrainedObject
        '''
        self.trainedObjects.append(trainedObject)


    def __matchUsingBruteforce(self, desc1, desc2, r_threshold=0.75):
        res = []
        for i in xrange(len(desc1)):
            dist = anorm(desc2 - desc1[i])
            n1, n2 = dist.argsort()[:2]
            r = dist[n1] / dist[n2]
            if r < r_threshold:
                res.append((i, n1))
        return np.array(res)


    def __matchUsingFlann(self, desc1, desc2, r_threshold=0.6):
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


    def __matchWithGivenflann(self, desc1, flannIndex, r_threshold=0.4):
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



    def matchObject(self, image, matchMethod="flann", useRansac = 1, surfThreshold=None):
        '''
        Finds best match for each object in the database.
        
        @param image: Image with object(s) to be found.
        @param matchMetod: flann or brute to select the matcher
        @param useRansac: 1/0 defining the optional use of RANSAC in homography matrix search.
        @param surfThreshold: Threshold for Hessian detector in SURF method used for training the objects.
        This method adapts however this threshold automatically basing on the read from each TrainedObject.
          
        @return: List of tuples (TrainedObject, bestMatchOrientationIndex, 
                                homographyStatus, homographyMatrix,
                                (matchedPointsInTrained, matchedPointsInTest) )
        '''
        # create new surf extractor only if needed
        if (surfThreshold is not None) and (surfThreshold != self.surfThreshold):
            self.surfThreshold = surfThreshold
            self.surf = cv2.SURF(self.surfThreshold)

        kp, desc = self.surf.detect(image, None, False)
        print "Found SURF features of the passed image"

        desc.shape = (-1, self.surf.descriptorSize())
        print "Created shape from descriptor"

        flannIndex = cv2.flann_Index(desc, self.flann_params)
        print "Found flann index"

        # list of (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)        
        bestMatches = list()

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
            bestMatchObject = None
            ind = 0

            for orientation in trainedObject.orientations:
                # we are using flannMatcher, can change to bruteForce'''
                if matchMethod == "flann":
                    matchResult = self.__matchWithGivenflann(orientation[2], flannIndex) # optimized with preGenerated FlannIndex
                else:
                    matchResult = self.__matchUsingBruteforce(orientation[2], desc) # we can use Brute
                    
                if len(matchResult) > 10:
                
                    matched_p1 = np.array([orientation[1][i].pt for i, j in matchResult])
                    matched_p2 = np.array([kp[j].pt for i, j in matchResult])

                    #print len(matched_p1), len(matched_p2)


                    H, status = cv2.findHomography(matched_p1, matched_p2, (0, cv2.RANSAC)[useRansac], 5.0)
                    #print "Orientation name: ", orientation[0].name
                    #print '%d / %d  inliers/matched' % (np.sum(status), len(status))

                    if ((bestMatchObject is None and np.sum(status) > 0)
                        or (np.sum(status) > np.sum(bestMatchObject[2])
                        or (np.sum(status) == np.sum(bestMatchObject[2]) and len(status) > len(bestMatchObject[2])))
                        ) :
                        bestMatchObject = (trainedObject, ind, status, H, (matched_p1, matched_p2))

                ind += 1

            # appends to the results the best match for each TrainedObject
            if bestMatchObject is not None:
                bestMatches.append(bestMatchObject)

        return bestMatches

