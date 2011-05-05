'''
Created on 04-05-2011

@author: Piotr
'''
import unittest
import os

from ImageDescription import ImageDescription

class ImageDescriptionReader(object):
    '''
    Reads the ImageDescription from stream.
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def read(self,fileStream):
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
        
        # seventh line is rotate
        p = float(lines[7])
        q = float(lines[8])
        r = float(lines[9])
        
        # now data
        #numberOfPoints = int(lines[11])
        points = []
        
        return ImageDescription(name,x,y,z,p,q,r,points)

class ImageDescriptionReaderUnitTests(unittest.TestCase):
    def setUp(self):
        # set up example data
        self.name = "sample_image"
        self.x = 0.0
        self.y = 0.5
        self.z = 0.75
        self.p = 0.0
        self.q = 0.25
        self.r = 0.85
        self.points = [0.0, 1.0, 2.0, 3.0]
        
        sequence = """@name
sample_image
@translate
0
0.5
0.75
@rotate
0
0.25
0.85
@data
2
0.0 1.0
2.0 3.0
"""
        self.expectedImage = ImageDescription(self.name,self.x,self.y,self.z,
                                     self.p,self.q,self.r,self.points)
        
        self.fileName = "some_file_name"
        with open(self.fileName,'w') as file:
            file.writelines(sequence)
            file.close()
        pass
    
    def tearDown(self):
        os.remove(self.fileName)
        pass       
    
    def testReadingNormalFileGetsTheProperValues(self):
        '''
        reading the file hardcoded gets the proper values
        '''
        
        # set up the file with such string
        with open(self.fileName,'r') as file:
            # read this file using reader
            reader = ImageDescriptionReader()
            readImage = reader.read(file)
        
        print readImage
        print self.expectedImage
        
        # compare the image objects
        self.assertEqual(self.expectedImage, readImage, "The values should be identical")
        pass 
    
if (__name__ == 'main'):
    unittest.main(verbosity=2)