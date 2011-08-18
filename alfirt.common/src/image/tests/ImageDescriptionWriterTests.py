'''
Created on Aug 18, 2011

@author: Piotr
'''
import unittest
from image.ImageDescription import ImageDescription
from image.ImageDescriptionWriter import ImageDescriptionWriter

import os

class ImageDescriptionWriterUnitTests(unittest.TestCase):

    def setUp(self):
        self.fileName = "test_file_name"
        with open(self.fileName, 'w') as fileStream:
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
            2.0
            0.0 1.0
            2.0 3.0
            """
        self.expectedString = self.expectedString.replace("    ", "")

    def tearDown(self):
        os.remove(self.fileName)

    def testOutputWithAllElement(self):
        '''
        tests if the output stream is good when parameters passed 
        are good
        '''
        # get the image description and the writer
        imageDesc = ImageDescription(self.name, self.x, self.y, self.z,
                                     self.p, self.q, self.r, self.points)
        imageWriter = ImageDescriptionWriter()

        #get the string steam
        with open(self.fileName, 'r+') as fileStream:
            imageWriter.write(fileStream, imageDesc)

        # read this file
        with open(self.fileName, 'r+') as fileStream:
            allLines = ''.join(fileStream.readlines())
            fileStream.close()

        self.assertEqual(self.expectedString, allLines , "Provided strings should be identical")


if (__name__ == 'main'):
    unittest.main(verbosity=2)



