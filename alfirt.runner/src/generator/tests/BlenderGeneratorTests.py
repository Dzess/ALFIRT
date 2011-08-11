'''
Created on Jun 18, 2011

@author: Piotr
'''
import unittest
from generator.BlenderGenerator import BlenderGenerator
from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose

class BlenderGeneratorTests(unittest.TestCase):
    '''
        High level generator tests.
    '''


    def setUp(self):
        s = """
        
        """

        self.expecetdFileString = s.replace(' ', '')


    def tearDown(self):
        pass


    def test_single_file_generation(self):
        '''
            Assumes that the Generator Descriptor is already created, then tests
            the code against the BlenderGenerator to produce the output file which 
            match the assertions.
        '''

        camera = ObjectPose([0, 0, 0], [0, 0, 0])
        anchor = ObjectPose([1, 1, 1], [0, 0, 0])

        sDesc = SceneDescription(camera, anchor)

        gen = BlenderGenerator()
        result = gen.prepareRender(sDesc)

        # assert the resulting file with the mock up in the upper code
        self.assertEqual(result, self.expecetdFileString, "The generated files should be identical")


if __name__ == "__main__":
    unittest.main()
