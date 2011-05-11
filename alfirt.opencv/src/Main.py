'''
Created on 05-05-2011

@author: Ankhazam
'''

import cv

if __name__ == '__main__':
    print "OpenCV Test"
    
    cv.NamedWindow("a_window", cv.CV_WINDOW_AUTOSIZE)
    image=cv.LoadImage("D:\Downloads\prezent.png", cv.CV_LOAD_IMAGE_COLOR) #Load the image
    font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
    cv.ShowImage("a_window", image) #Show the image
    cv.waitKey()
    pass