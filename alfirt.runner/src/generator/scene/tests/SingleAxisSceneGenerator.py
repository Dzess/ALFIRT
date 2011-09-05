'''
Created on Aug 27, 2011

@author: Piotr
'''
import unittest
from math import radians
from generator.scene.SceneGenerators import SingleAxisSceneGenerator
from generator.data.ObjectPose import ObjectPose
from generator.data.GeneratorInterval import GeneratorInterval
from mockito.mockito import verify
from generator.data.SceneDescription import SceneDescription
from generator.scene.tests.SceneGeneratorTestsBase import SceneGeneratorTestsBase

class SingleAxisSceneGeneratorTests(unittest.TestCase, SceneGeneratorTestsBase):
    '''
        Testing generation of the scene using the 
        @see: SingleAxisSceneGenerator
    '''

    def test_rotation_by_3_points(self):
        '''
            Testing rotating camera around exactly the way described 
            on the resources/testing_rotations.
        '''

        # setting up initial positions
        initTranslate = [5, 0, 5]
        initRotate = [radians(60), radians(0), radians(90)]

        alfa = GeneratorInterval(0, 180, 90)
        beta = GeneratorInterval(5, 5)

        generatorDesc = self.getGeneratorDescription(alfa, beta, initTranslate)

        initCamera = ObjectPose(initTranslate, initRotate)
        initAnchor = self.getInitAnchor()

        # setting up expected scenes

        # scene 1 (initial)
        translate_1 = initTranslate
        rotate_1 = initRotate
        expected_scene_1 = SceneDescription(ObjectPose(translate_1, rotate_1), initAnchor)

        # scene 2
        translate_2 = [0, 5, 5]
        rotate_2 = [radians(60), radians(0), radians(180)]
        expected_scene_2 = SceneDescription(ObjectPose(translate_2, rotate_2), initAnchor)

        # scene 3
        translate_3 = [-5, 0, 5]
        rotate_3 = [radians(60), radians(0), radians(270)]
        expected_scene_3 = SceneDescription(ObjectPose(translate_3, rotate_3), initAnchor)

        # act
        generator = SingleAxisSceneGenerator(
                                             generatorDesc=generatorDesc,
                                             initCamera=initCamera,
                                             initAnchor=initAnchor)
        scenes = generator.prepareScenes()

        # verify calling generator intervals
        verify(generatorDesc, atleast=1).alfa
        verify(generatorDesc, atleast=1).beta

        self.assertEqual(3, len(scenes), "Number of scenes generated should be equal to 3")

        # assertions about each scene values
        self.assertEqual(scenes[0], expected_scene_1,
                         self.getDifferMessage(expected_scene_1, scenes[0]))
        self.assertEqual(scenes[1], expected_scene_2,
                         self.getDifferMessage(expected_scene_2, scenes[1]))
        self.assertEqual(scenes[2], expected_scene_3,
                         self.getDifferMessage(expected_scene_3, scenes[2]))


    def test_rotation_by_no_values(self):
        # TODO: code this test up !
        pass


if __name__ == "__main__":
    unittest.main()
