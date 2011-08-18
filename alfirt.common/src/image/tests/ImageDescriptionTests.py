'''
Created on Aug 18, 2011

@author: Piotr
'''
from image.ImageDescription import ImageDescription
import unittest

class ImageDescriptionUnitTests(unittest.TestCase):
        def setUp(self):
            # set up example data
            self.name = "sample_image"
            self.x = 0
            self.y = 0.5
            self.z = 0.75
            self.p = 0
            self.q = 0.25
            self.r = 0.85
            self.points = [0.0, 1.0, 2.0, 3.0]

        def testEqualityOnAllProperties(self):
            '''
            tests the equality comparer
            '''
            imag1 = ImageDescription(self.name, self.x, self.y, self.z, self.p, self.q, self.r, self.points)
            imag2 = ImageDescription(self.name, self.x, self.y, self.z, self.p, self.q, self.r, self.points)

            self.assertEqual(imag1, imag2, "The images are equal")

        def testEqualityComparisionOnPoints(self):
            '''
            checks if the points are used for comparison
            '''
            points2 = [0.0, 2.0]
            imag1 = ImageDescription(self.name, self.x, self.y, self.z, self.p, self.q, self.r, self.points)
            imag2 = ImageDescription(self.name, self.x, self.y, self.z, self.p, self.q, self.r, points2)

            self.assertNotEqual(imag1, imag2, "Image description are different because of the mask")

        def testNotSameInstanceBeingCompared(self):
            '''
            check if passing some other object and ImageDescription results in nice False message
            '''
            imag1 = ImageDescription(self.name, self.x, self.y, self.z, self.p, self.q, self.r, self.points)
            imag2 = [2.0, 3.0]
            self.assertNotEqual(imag1, imag2, "Thie values should not be equal, nor exception should be thrown")

        def testAllAxisArgumentsMustBeANumber(self):
            '''
            checks if the values provided within the axis parameters are numbers
            '''
            value = "some_text_which_is_not_a_number"
            numberParameters = [ 'x', 'y', 'z', 'p', 'q', 'r']
            for index in range(0, len(numberParameters)):
                args = [self.name, self.x, self.y, self.z, self.p, self.q, self.r, self.points]
                # manipulate argument list to get the specified pa
                args[index + 1] = value
                with self.assertRaises(ValueError) :
                    ImageDescription(*args)

        def testOutputWithOddNumberOfPonts(self):
            '''
            should raise an error when the number of points passed to the image is odd
            '''
            # odd number of points
            self.points = [1.0, 2.0, 3.0]

            with self.assertRaises(ValueError) :
                ImageDescription(self.name, self.x, self.y, self.z, self.p, self.q, self.r, self.points)

        def testNormalDataShouldGoWithoutProblem(self):
            '''
            tests if the normal data passes the constructor
            '''
            ImageDescription(self.name, self.x, self.y, self.z,
                            self.p, self.q, self.r, self.points)

if (__name__ == 'main'):
    unittest.main(verbosity=2)

