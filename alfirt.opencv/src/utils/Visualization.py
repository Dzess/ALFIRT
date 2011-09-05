'''
Created on 05-09-2011

@author: Ankhazam
'''

import cv2
from numpy.ma.core import cos, sin


class Visualization(object):
    '''
    Contains methods useful for drawing processed images
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
                
    def showNewImageWindow(self, image, windowName):
        '''
        Creates a new windows with given image.
        @param image: OpenCV read numpy array containing the image.
        @param windowName: Name of window.
        '''
        cv2.namedWindow(windowName, cv2.CV_WINDOW_AUTOSIZE)
        cv2.imshow(windowName, image) #Show the image

    
    def findSURF(self, image, threshold=400):
        '''
        Finds SURF features in given image.
        
        @param image: image to be searched for features
        @param threshold: level used for features detection (best between 400-1200)
        @return: Tuple of (keypoints, descriptors) aquired from surf extractor.
        '''  
        if  cv2.cv.fromarray(image).type != cv2.CV_8UC1:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            img = image.copy()            
        
        surf = cv2.SURF(threshold)
        keypoints, descriptors = surf.detect(img, None, False)
        
        #drawing the keypoints
        img = image.copy()
        for key in keypoints :
            self.drawKeypoint(img, key)
        self.showNewImageWindow(img, "SURFED")
        
        descriptors.shape = (-1, surf.descriptorSize())
        return keypoints, descriptors
    
        
    def drawKeypoint(self, image, keypoints):
        '''
        Draws SURF extracted keypoints fully emphasising discovered features (center,response,angle).
        
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
        

