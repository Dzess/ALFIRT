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

        
    def printGoodFeatures(self, image=None):
        if image is None:
            image = self.image

        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imgColour = image.copy()
        corners = cv2.goodFeaturesToTrack(img, 100, 0.04, 1)
        for (x, y) in np.float32(corners.reshape(-1, 2)):
            cv2.circle(imgColour, (x, y), 3, (0, 0, 255, 0), 1)
            #print "good feature at", x, y
        
        self.showNewImageWindow(imgColour, "Good features")
        return corners
        
    def cannyTheImage(self, image=None):
        if image is None:
            image = self.image
            
        if  cv2.cv.fromarray(image).type != cv2.CV_8UC1:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            img = image.copy()
        img = cv2.Canny(img, 50, 200)
        self.showNewImageWindow(img, "canny")
        return img
        
    def findObjects(self, image=None):
        if image is None:
            image = self.image

        if  cv2.cv.fromarray(image).type != cv2.CV_8UC1:
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            img = image.copy()

        (_, img) = cv2.threshold(img, cv2.mean(img)[0], 255, cv2.THRESH_BINARY)
        self.showNewImageWindow(img, "thresholded")
        
        (contours, _) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img = image.copy()
        
        for contour in contours:
            #print contour-
            cv2.drawContours(image, contour, -1, (0, 0, 255))
            rect = cv2.boundingRect(contour)
            


        
        self.showNewImageWindow(image, "findObjects")
        
        return contours


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
        if len(args) != 1:
            print "Required path to image file missing."
            sys.exit()
        print "Testing mode"
        recognition = NaiveRecognition(options.runType, args[0], None)
        
    else:
        if len(args) != 2:
            print "Required paths to image and expected output files missing."
            sys.exit()
        print "Learning mode"
        recognition = NaiveRecognition(options.runType, args[0], args[1])
        
    
    print recognition.findObjects()
    print recognition.printGoodFeatures()
    while cv2.waitKey() is not 27:
        pass
       
    

