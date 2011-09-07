'''
Created on 05-09-2011

@author: Ankhazam
'''

import cv2
from numpy.ma.core import cos, sin
import numpy as np


class Utils(object):
    '''
    Contains methods useful for drawing processed images
    '''

    def __init__(self, surfThreshold=400):
        '''
        Creates the utilities with default SURF extractor
        
        @param surfThreshold: Default HessianThreshold for SURF extractor.
        '''
        self.threshold = surfThreshold
        self.surf = cv2.SURF(self.threshold)

    def showNewImageWindow(self, image, windowName):
        '''
        Creates a new windows with given image.
        @param image: OpenCV read numpy array containing the image.
        @param windowName: Name of window.
        '''
        cv2.namedWindow(windowName, cv2.CV_WINDOW_AUTOSIZE)
        cv2.imshow(windowName, image) #Show the image


    def findSURF(self, image, threshold=None):
        '''
        Finds SURF features in given image.
        
        @param image: image to be searched for features
        @param threshold: level used for features detection (best between 400-1200)
        @return: Tuple of (keypoints, descriptors) acquired from surf extractor.
        '''
        if  cv2.cv.fromarray(image).type != cv2.CV_8UC1:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            img = image

        # create new surf extractor only if needed
        if (threshold is not None) and (threshold != self.threshold):
            self.threshold = threshold
            self.surf = cv2.SURF(threshold)

        keypoints, descriptors = self.surf.detect(img, None, False)

        descriptors.shape = (-1, self.surf.descriptorSize())
        return keypoints, descriptors


    def drawKeypoints(self, image, keypoints):
        '''
        Draws SURF extracted keypoints fully emphasizing discovered features (center,response,angle).
        
        @param image: Image to draw on.
        @param keypoints: List of keypoints to be drawn.
        '''
        for keypoint in keypoints:
            # fetch basic info
            radius = int(keypoint.size / 2)
            center = (int(keypoint.pt[0]), int(keypoint.pt[1]))

            color = (0, 0, 255)
            # draw circle in center
            cv2.circle(image, center, radius, color)

            # draw orientation
            if keypoint.angle != -1 :
                angleRad = keypoint.angle * cv2.cv.CV_PI / 180
                destPoint = (int(cos(angleRad) * radius) + center[0], int(sin(angleRad) * radius) + center[1])
                cv2.line(image, center, destPoint, color)
            else:
                cv2.circle(image, center, 1, color)

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
