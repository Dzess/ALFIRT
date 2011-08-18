'''
Created on Aug 15, 2011

@author: Piotr
'''
import unittest
from utils.PolarSystem import PolarSystem


class PolarSystemUnitTests(unittest.TestCase):
    '''
        Tests if the changing for polar system works good
    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def __runToPolar(self, x, y, z, expectedAlfa, expectedBeta, expectedRadius):
        result = PolarSystem.toPolar(x, y, z)
        self.assertEqual(result.alfa, expectedAlfa)
        self.assertEqual(result.beta, expectedBeta)
        self.assertEqual(result.radius, expectedRadius)

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

        self.__runToPolar(x, y, z, expectedAlfa, expectedBeta, expectedRadius)

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

        self.__runToPolar(x, y, z, expectedAlfa, expectedBeta, expectedRadius)

    #TODO: write more from_polar testing

if (__name__ == 'main'):
    unittest.main(verbosity=2)
