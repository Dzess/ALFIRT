'''
Created on Aug 10, 2011

@author: Piotr
'''
import unittest
from generator.data.GeneratorDescription import GeneratorDescription
from generator.data.GeneratorInterval import GeneratorInterval
from generator.data.SceneDescription import SceneDescription
from generator.SceneGenerator import SceneGenerator


class Test(unittest.TestCase):


    def setUp(self):
        self.gDesc = GeneratorDescription()


    def tearDown(self):
        pass



    def setGeneratorDescription(self, int1, int2):
        self.gDesc.alfa = int2
        self.gDesc.beta = int1
        self.gDesc.radius = int1

    def test_single_description_generation(self):
        '''
            Checks if the SceneGenerator creates valid camera and anchor setting basing on 
            the passed GeneratorDescription
        '''

        # the interval pinpoints one position of camera
        interval = GeneratorInterval(5, 5, 0)

        #expected camera state is not meaningful now
        expectedScene = SceneDescription(None, None)

        # initialization of the gDesc 
        self.setGeneratorDescription(interval, interval)

        gen = SceneGenerator(self.gDesc)
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
        self.setGeneratorDescription(interval2, interval1)

        gen = SceneGenerator(self.gDesc)
        scenes = gen.prepareScenes()

        self.assertEqual(type(scenes), type([]), "The returned element should be list")
        self.assertEqual(len(scenes), 2, "Two scenes should be returned")


if __name__ == "__main__":
    unittest.main()
