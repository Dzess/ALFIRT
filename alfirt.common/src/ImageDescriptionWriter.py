'''
Created on 04-05-2011

@author: Piotr Jessa
'''

import os
import unittest

from ImageDescription import ImageDescription


class ImageDescriptionWriter(object):
    '''
    Writes the ImageDescription class to the file stream
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def writeline(self,text):
        '''
        writes the text ended with \n to the stream
        '''
        self.stream.write(text)
        self.stream.write('\n')

    def write(self, stream, imageDescription):
        '''
        writes the image description formatted into stream
        '''
        self.stream = stream
        
        self.writeline("@name")
        self.writeline(imageDescription.name)
        
        self.writeline("@translate")
        self.writeline(str(imageDescription.x))
        self.writeline(str(imageDescription.y))
        self.writeline(str(imageDescription.z))
        
        self.writeline("@rotate")
        self.writeline(str(imageDescription.p))
        self.writeline(str(imageDescription.q))
        self.writeline(str(imageDescription.r))
        
        self.writeline("@data")
        self.writeline(str(len(imageDescription.points)/2))
        for i in range(1,len(imageDescription.points),2):
            stream.write(str(imageDescription.points[i-1]))
            stream.write(' ')
            self.writeline(str(imageDescription.points[i]))
        
        
#===============================================================================
# UnitTests
#===============================================================================   
class ImageDescriptionWriterUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.fileName ="test_file_name"
        with open(self.fileName,'w') as fileStream:
            fileStream.close()
            
        # set up example data
        self.name = "sample_image"
        self.x = 0
        self.y = 0.5
        self.z = 0.75
        self.p = 0
        self.q = 0.25
        self.r = 0.85
        self.points = [0.0, 1.0, 2.0, 3.0]
        
        self.expectedString = """@name
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
    
    def tearDown(self):
        os.remove(self.fileName)
            
    def testOutputWithAllElement(self):
        '''
        tests if the output stream is good when parameters passed 
        are good
        '''
        # get the image description and the writer
        imageDesc = ImageDescription(self.name,self.x,self.y,self.z,
                                     self.p,self.q,self.r,self.points)
        imageWriter = ImageDescriptionWriter()
        
        #get the string steam
        with open(self.fileName,'r+') as fileStream:
            imageWriter.write(fileStream,imageDesc)
        
        # read this file
        with open(self.fileName,'r+') as fileStream:
            allLines = ''.join(fileStream.readlines())
            fileStream.close()
        
        self.assertEqual(self.expectedString, allLines , "Provided strings should be identical")
        pass
    
#===============================================================================
# Runner for unittest
#===============================================================================   
if (__name__ == 'main'):
    unittest.main(verbosity=2)
    
    
        