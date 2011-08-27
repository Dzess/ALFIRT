'''
Created on Aug 27, 2011

@author: Piotr
'''
import unittest
from math import radians
from math import sqrt
from generator.scene.SceneGenerators import SingleAxisSceneGenerator
from generator.data.ObjectPose import ObjectPose
from mockito.mocking import mock
from generator.data.GeneratorInterval import GeneratorInterval
from mockito.mockito import verify
from generator.data.SceneDescription import SceneDescription

class SingleAxisSceneGeneratorTests(unittest.TestCase):
    '''
        Testing generation of the scene using the 
        @see: SingleAxisSceneGenerator
    '''


    def __getDifferMessage(self, expected, actual):
        string = "Scene differs: expected:" + str(expected) + "\n"
        string += "but got " + str(actual) + "\n"
        return  string


    def test_rotation_by_3_points(self):
        '''
            Testing rotating camera around exactly the way described 
            on the resources/testing_rotations.
        '''

        # setting up initial positions
        initTranslate = [5, 0, 5]
        initRotate = [radians(60), radians(0), radians(90)]

        alfa = GeneratorInterval(0, 180, 90)
        beta = None
        radius_sqrt = sqrt(25 + 25)
        radius = GeneratorInterval(start=radius_sqrt, stop=radius_sqrt)
        generatorDesc = mock(mocked_obj=None, strict=True)

        generatorDesc.alfa = alfa
        generatorDesc.beta = beta
        generatorDesc.radius = radius
        initCamera = ObjectPose(initTranslate, initRotate)
        initAnchor = ObjectPose([0, 0, 0], [0, 0, 0])

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
        generator = SingleAxisSceneGenerator(generatorDesc, initCamera, initAnchor=initAnchor)
        scenes = generator.prepareScenes()

        # verify calling generator intervals
        verify(generatorDesc, atleast=1).alfa
        verify(generatorDesc, atleast=1).beta

        self.assertEqual(3, len(scenes), "Number of scenes generated should be equal to 3")

        # assertions about each scene values
        self.assertEqual(scenes[0], expected_scene_1,
                         self.__getDifferMessage(expected_scene_1, scenes[0]))
        self.assertEqual(scenes[1], expected_scene_2,
                         self.__getDifferMessage(expected_scene_2, scenes[1]))
        self.assertEqual(scenes[2], expected_scene_3,
                         self.__getDifferMessage(expected_scene_3, scenes[2]))


    def test_rotation_by_no_values(self):

        pass


if __name__ == "__main__":
    unittest.main()
