'''
Created on 30-08-2011

@author: Ankhazam

Based on find_obj.py OpenCV2 sample
'''

import numpy as np
import cv2
from common import anorm

class ORBFlannMatcher(object):
    '''
    Main recognition and training module.
    '''

    detector = cv2.FastFeatureDetector(16, True)
    detector = cv2.GridAdaptedFeatureDetector(detector)
    extractor = cv2.DescriptorExtractor_create('ORB')

    FLANN_INDEX_KDTREE = 1
    FLANN_INDEX_LSH    = 6
    flann_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 12, # 12
                   key_size = 20,     # 20
                   multi_probe_level = 2) #2
    matcher = cv2.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)

    def __init__(self, trainedObjects):
        '''
        Constructor
        
        @param trainedObjects: List of @see: TrainedObject used as recognition DB
        '''
        self.trainedObjects = trainedObjects

    def addTrainedObject(self, trainedObject):
        '''
        Extends the loaded database with a new @see: TrainedObject
        '''
        self.trainedObjects.append(trainedObject)


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



    def matchObject(self, image, useRansac = 1):
        '''
        Finds best match for each object in the database.
        
        @param image: Image with object(s) to be found.
        @param useRansac: 1/0 defining the optional use of RANSAC in homography matrix search.

        @return: List of tuples (TrainedObject, bestMatchOrientationIndex, 
                                homographyStatus, homographyMatrix,
                                (matchedPointsInTrained, matchedPointsInTest) )
        '''


        # training the matcher for current test image
        self.matcher.clear()
        ref_kp = self.detector.detect(image)
        ref_kp, ref_desc = self.extractor.compute(image,ref_kp)
        self.matcher.add([ref_desc])
        

        # list of (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)        
        bestMatches = list()

        # simple searching for best matched orientation        
        for trainedObject in self.trainedObjects:

            # (TrainedObject, bestMatchOrientationIndex, homographyStatus, homographyMatrix)
            bestMatchObject = None
            ind = 0

            for orientation in trainedObject.orientations:
                
                raw_matches = self.matcher.knnMatch(orientation[2], 2)
                matches = []
                for m in raw_matches:
                    if len(m) == 2:
                        m1, m2 = m
                        if m1.distance < m2.distance * 0.7:
                            matches.append((m1.trainIdx, m1.queryIdx))
                
                if len(matches) > 10:
                
                    matched_p1 = np.float32( [ref_kp[i].pt for i, j in matches] )
                    matched_p2 = np.float32( [orientation[1][j].pt for i, j in matches] )

                    #print len(matched_p1), len(matched_p2)
                    H, status = cv2.findHomography(matched_p1, matched_p2, (0, cv2.RANSAC)[useRansac], 10.0)
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

