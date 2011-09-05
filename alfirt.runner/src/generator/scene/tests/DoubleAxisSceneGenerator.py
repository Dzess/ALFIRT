'''
Created on Aug 31, 2011

@author: Piotr
'''
import unittest
from generator.scene.tests.SceneGeneratorTestsBase import SceneGeneratorTestsBase


class DoubleAxisSceneGeneratorTests(unittest.TestCase, SceneGeneratorTestsBase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_generation_of_sinle_line_of_scenes(self):
        '''
            Using one level of vertical rotation: the output should be the same as the
            @see: SingleAxisSceneGenerator.
        '''
        self.fail("Not yet implemented")
        pass


    def test_generation_of_two_lines_of_scene(self):
        '''
            Should produce two lines of vertical rotation the output should be the 
            same as the two independent runs in @see: SingleAxisSceneGenerator.  
        '''
        self.fail("Not yet implemented")
        pass


if __name__ == "__main__":
    unittest.main()
