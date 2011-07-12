'''
Created on 05-05-2011

@author: Ankhazam
'''

import cv2
from optparse import OptionParser
import sys
import ImageDescription
import ImageDescriptionReader
import unittest

class NaiveRecognition(object):
    
    def __init__(self, type, imagePath, refImage):
        self.type = type
        self.imagePath = imagePath
        if self.type == "learn":
            if refImage is ImageDescription:
                self.refImage = refImage
            else:
                with open(refImage, 'r') as refFile:
                    reader = ImageDescriptionReader()
                    self.refImage = reader.read(refFile)
            
                
    def showImage(self):
        window_name = self.type
        cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)
        image = cv2.imread(self.imagePath)
        cv2.imshow(window_name, image) #Show the image
        cv2.waitKey()
        
    def printGoodFeatures(self):
        img = cv2.cv.LoadImageM(self.imagePath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        imgColour = cv2.cv.LoadImageM(self.imagePath)
        eig_image = cv2.cv.CreateMat(img.rows, img.cols, cv2.CV_32FC1)
        temp_image = cv2.cv.CreateMat(img.rows, img.cols, cv2.CV_32FC1)
        
        for (x, y) in cv2.cv.GoodFeaturesToTrack(img, eig_image, temp_image, 100, 0.04, 1.0, useHarris=True):
            cv2.cv.Circle(imgColour, (int(x), int(y)), 3, cv2.cv.Scalar(0, 0, 255, 0), thickness=2, lineType=8, shift=0)
            print "good feature at", x, y 
           
        window_name = self.type
        cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)                  
        cv2.cv.ShowImage(window_name, imgColour) #Show the image
        cv2.cv.WaitKey()        
        

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
        
    # recognition.showImage()
    recognition.printGoodFeatures()
       
    

