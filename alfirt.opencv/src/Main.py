'''
Created on 05-05-2011

@author: Ankhazam
'''

import cv2
import numpy as np
from optparse import OptionParser
import sys
from image.ImageDescription import ImageDescription
from image.ImageDescriptionReader import ImageDescriptionReader
import unittest
from copy import deepcopy
from numpy.ma.core import cos, sin
import samples.find_obj as SampleMatch


class NaiveRecognition(object):
    
    
    def __init__(self, runType, imagePath, refImage):
        
        self.runType = runType
        
        if self.runType == "learn":
            if refImage is ImageDescription:
                self.refImage = refImage
            else:
                with open(refImage, 'r') as refFile:
                    reader = ImageDescriptionReader()
                    self.refImage = reader.read(refFile)
                    
        self.loadImage(imagePath)
            
    def loadImage(self, newImagePath):
        self.image = cv2.imread(newImagePath)
        self.imagePath = newImagePath
        return self.image
                
    def showNewImageWindow(self, image, windowName):
        cv2.namedWindow(windowName, cv2.CV_WINDOW_AUTOSIZE)
        cv2.imshow(windowName, image) #Show the image

    
    def findSURF(self, image=None, threshold=400):
        if image is None:
            image = self.image
            
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
    
        
    def drawKeypoint(self, image, keypoint):
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
        


if __name__ == '__main__':
    print "OpenCV Learning Application"
    
    parser = OptionParser(usage="usage: %prog [options] [image_filename] [expected_output_file]")
    parser.add_option("-r", "--runType", action="store", dest="runType", type="str",
        help="Run selection learn|test. If \"learn\" is selected then expected output file path has to be provided.",
        default="test")
    (options, args) = parser.parse_args()
    
    if ((options.runType != "learn") & (options.runType != "test")):
        print "Invalid argument for -r option: " + options.runType
        sys.exit()
    elif (options.runType == "test"):
        if len(args) <= 1:
            print "Required path to image file missing."
            sys.exit()
        print "Testing mode"
        recognition = NaiveRecognition(options.runType, args[0], None)
        
    else:
        if len(args) <= 2:
            print "Required paths to image and expected output files missing."
            sys.exit()
        print "Learning mode"
        recognition = NaiveRecognition(options.runType, args[0], args[1])
        
    
    # matching stuff
    kp1, dsc1 = recognition.findSURF(recognition.loadImage(args[1]))
    kp2, dsc2 = recognition.findSURF(recognition.loadImage(args[2]))

    print 'img1 - %d features, img2 - %d features' % (len(kp1), len(kp2))
    
    while cv2.waitKey() is not 27:
        pass
       
    

