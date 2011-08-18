'''
Created on 04-05-2011

@author: Piotr
'''
import unittest
import os

from image.ImageDescription import ImageDescription

class ImageDescriptionReader(object):
    '''
    Reads the ImageDescription from stream.
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def read(self, fileStream):
        '''
        Reads the file searching for the elements, and returning the common image
        description format instance 
        '''
        lines = fileStream.readlines()
        # first line is @name
        name = lines[1].rstrip()
        # third line is @translate
        x = float(lines[3])
        y = float(lines[4])
        z = float(lines[5])

        # seventh line is @rotate
        p = float(lines[7])
        q = float(lines[8])
        r = float(lines[9])

        # now @data
        numberOfPoints = int(lines[11])
        points = []
        for i in range(0, numberOfPoints, 1):
            words = lines[12 + i].split(' ')
            points.append(float(words[0]))
            points.append(float(words[1]))

        return ImageDescription(name, x, y, z, p, q, r, points)
