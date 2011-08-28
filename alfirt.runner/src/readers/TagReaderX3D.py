'''
Created on 10-05-2011

@author: Piotr
'''
import os
import logging
from lxml import etree

from generator.data.SceneDescription import SceneDescription
from readers.ParserX3D import ParserX3D

class TagReaderX3D(object):
    '''
    Reads the data stream gets the ALFIRT tags from XML document. 
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.parser = ParserX3D()


    def readScene(self, fileName):
        '''
        Reads fileName in .x3d format and returns the data from ALFRT tags.
        @param fileName: the path to the .x3d fileName tagged with ALFIRT attributes. 
        @return: the @see: SceneDescription object with anchor. Camera object is optional.
        
        '''
        if (fileName == None) :
            raise ValueError("The fileName attribute is mandatory")

        if not os.path.exists(fileName):
            raise ValueError("The fileName provided does not exists")

        logging.info("Reading the input model file: '" + fileName + "'")

        # using XML broad available library read fileName
        tree = etree.parse(fileName)

        # Get the anchor element
        anchor = self.parser.getAnchorElement(tree)

        # Get the camera element
        camera = self.parser.getCameraElement(tree)

        result = SceneDescription(anchor=anchor, camera=camera)

        return result

