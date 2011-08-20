'''
Created on Aug 20, 2011

@author: Piotr
'''
import unittest
from BlenderRunner import BlenderRunner
from generator.data.GeneratorDescription import GeneratorDescription
from mockito.mock import Mock
from generator.BlenderGenerator import BlenderGenerator


class BlenderRunnerTests(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_running_blender(self):
        '''
            Test if the blender script is invoked correctly
        '''
        gDesc = GeneratorDescription()
        bGen = BlenderGenerator(gDesc)
        sGen = Mock()

        runner = BlenderRunner(gDesc, sGen, bGen)
        runner.execute()

if __name__ == "__main__":
    unittest.main()
