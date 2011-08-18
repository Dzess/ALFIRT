'''
Created on Aug 10, 2011

@author: Piotr
'''
import unittest
from generator.data.GeneratorDescription import GeneratorDescription
from generator.data.GeneratorInterval import GeneratorInterval
from generator.data.SceneDescription import SceneDescription
from generator.scene.SingleAxisSceneGenerator import SingleAxisSceneGenerator
from generator.data.ObjectPose import ObjectPose


class SingleAxisSceneGeneratorTests(unittest.TestCase):
    '''
        Unit Tests for class @see: SingleAxisSceneGenerator
    '''

    def setUp(self):
        self.gDesc = GeneratorDescription()
        self.initCamera = ObjectPose([1, 0, 1], [0, 0, 0])

    def tearDown(self):
        pass



    def __setGeneratorDescription(self, int1, int2):
        self.gDesc.alfa = int2
        self.gDesc.beta = int1
        self.gDesc.radius = int1

    def test_single_description_generation(self):
        '''
            Checks if the SingleAxisSceneGenerator creates valid camera and anchor setting basing on 
            the passed GeneratorDescription
        '''

        # the interval pinpoints one position of camera
        interval = GeneratorInterval(5, 5, 0)

        #expected camera state is not meaningful now
        expectedScene = SceneDescription(None, None)

        # initialization of the gDesc 
        self.__setGeneratorDescription(interval, interval)

        gen = SingleAxisSceneGenerator(self.gDesc, self.initCamera)
        scenes = gen.prepareScenes()

        self.assertEquals(type(scenes) , type([]), "The returned elements should be list")
        self.assertEqual(len(scenes), 1, "One scene should be returned")
        self.assertEqual(scenes[0], expectedScene, "The scenes should be identical")

    def test_multiple_scene_creation(self):
        '''
            Check if the providing the intervals the proper number of scenes is generated
        '''
        interval1 = GeneratorInterval(1, 2, 1)
        interval2 = GeneratorInterval(start=2, stop=2)

        # pass to the generator
        self.__setGeneratorDescription(interval2, interval1)

        gen = SingleAxisSceneGenerator(self.gDesc, self.initCamera)
        scenes = gen.prepareScenes()

        self.assertEqual(type(scenes), type([]), "The returned element should be list")
        self.assertEqual(len(scenes), 2, "Two scenes should be returned")

    def test_single_scene_genration_proper_values(self):
        '''
            Checks if the generated scene has the proper values basing on the
            GeneratorDescriptor
        '''
        self.fail("Not yet implemented")

    def test_single_scene_generation_proper_values_triangulation(self):
        '''
            Same as the test about checks the generated values for
            the another set of data
        '''
        self.fail("Not yet implemented")
        pass

if __name__ == "__main__":
    unittest.main()
