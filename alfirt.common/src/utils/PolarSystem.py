'''
Created on 12-05-2011

@author: Piotr
'''
import unittest

class PolarSystem(object):
    '''
    Transforms from 3D polar system to karthesian one.
    '''

    def __init__(self):
        '''
        Constructor. Not usable.
        '''

    @classmethod
    def toPolar(cls, x, y, z):
        '''
        Transforms from vector space x,y,z to polar system.
        @param x: x coordinate in vector space
        @param y: y coordinate in vector space
        @param z: z coordinate in vector space   
        
        @attention: Assumes that the center of the polar system vector [0,0,0]
        '''
        pass

    @classmethod
    def fromPolar(cls, alfa, beta, radius):
        '''
        Transform from alfa, beta polar space into x,y,z vector space.
        
        @param alfa: angle in degrees [0,360] on the z based space
        @param beta: angle in degrees [0,360] on the x based space
        @param radius: the radius coordinate   
        @attention: Assumes that the center of the polar system vector [0,0,0]
        
        '''

        pass

#===============================================================================
#  UnitTests
#===============================================================================
class PolarSystemUnitTests(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass



    def runToPolar(self, x, y, z, expectedAlfa, expectedBeta, expectedRadius):
        result = PolarSystem.toPolar(x, y, z)
        self.assertEqual(result.alfa, expectedAlfa, "The alfa should be 0")
        self.assertEqual(result.beta, expectedBeta, "The alfa should be 0")
        self.assertEqual(result.radius, expectedRadius, "The alfa should be 0")

    def test_toPolar_case_1(self):
        '''
        Transforms [0,0,0] vector into polar space
        '''
        x = 0
        y = 0
        z = 0

        expectedAlfa = 0
        expectedBeta = 0
        expectedRadius = 0

        self.runToPolar(x, y, z, expectedAlfa, expectedBeta, expectedRadius)
        pass

    def test_toPolar_case_2(self):
        '''
        Transforms vector [1,2,3] into the proper value which is:
        
        '''
        x = 1
        y = 2
        z = 3

        # TODO: add support for that definitions
        expectedAlfa = 0
        expectedBeta = 0
        expectedRadius = 0

        self.runToPolar(x, y, z, expectedAlfa, expectedBeta, expectedRadius)
        pass

#===============================================================================
#  Test runner
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)
