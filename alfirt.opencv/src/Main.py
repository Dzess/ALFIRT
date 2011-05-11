'''
Created on 05-05-2011

@author: Ankhazam
'''

import cv
import sys
from optparse import OptionParser

if __name__ == '__main__':
    print "OpenCV Learning Application"
    
    parser = OptionParser(usage="usage: %prog [options] [image_filename] [expected_output_file]")
    parser.add_option("-r", "--runType", action="store", dest="runType", type="str",
        help="Run selection learn|test. If \"learn\" is selected then expected output file path has to be provided.",
        default="test")
    (options, args) = parser.parse_args()
    
    if ((options.runType != "learn") & (options.runType != "test")):
        print "Invalid argument for -r option: " +options.runType
        sys.exit()
    elif (options.runType == "test"):
        if len(args)!= 1:
            print "Required path to image file missing."
            sys.exit()
        print "Testing mode"
    else:
        if len(args)!= 2:
            print "Required paths to image and expected output files missing."
            sys.exit()
        print "Learning mode"
    
    
    # Running opencv
    window_name = options.runType
    cv.NamedWindow(window_name, cv.CV_WINDOW_AUTOSIZE)
    image=cv.LoadImage(args[0], cv.CV_LOAD_IMAGE_COLOR) #Load the image
    cv.ShowImage(window_name, image) #Show the image
    cv.waitKey()
    pass