'''
Created on Aug 31, 2011

@author: Piotr
'''
import unittest
from generator.scene.tests.SceneGeneratorTestsBase import SceneGeneratorTestsBase
from mockito.mockito import verify
from math import radians, sin, cos
from generator.data.GeneratorInterval import GeneratorInterval
from generator.data.ObjectPose import ObjectPose
from generator.data.SceneDescription import SceneDescription
from generator.scene.SceneGenerators import DoubleAxisSceneGenerator


class DoubleAxisSceneGeneratorTests(unittest.TestCase, SceneGeneratorTestsBase):

    def setUp(self):
        self.initTranslate = [5, 0, 0]
        self.initRotate = [radians(60), radians(0), radians(90)]

        self.alfa = GeneratorInterval(0, 180, 90)
        self.radius = 5

    def tearDown(self):
        pass


    def test_generation_of_sinle_line_of_scenes(self):
        '''
            Using one level of vertical rotation: the output should be the same as the
            @see: SingleAxisSceneGenerator.
        '''

        # no beta moves too much
        beta = GeneratorInterval(0, 0)

        generatorDesc = self.getGeneratorDescription(self.alfa, beta, self.initTranslate)

        initCamera = ObjectPose(self.initTranslate, self.initRotate)
        initAnchor = self.getInitAnchor()

        # scene 1 (initial)
        translate_1 = self.initTranslate
        rotate_1 = self.initRotate
        expected_scene_1 = SceneDescription(ObjectPose(translate_1, rotate_1), initAnchor)

        # scene 2
        translate_2 = [0, 5, 0]
        rotate_2 = [radians(60), radians(0), radians(180)]
        expected_scene_2 = SceneDescription(ObjectPose(translate_2, rotate_2), initAnchor)

        # scene 3
        translate_3 = [-5, 0, 0]
        rotate_3 = [radians(60), radians(0), radians(270)]
        expected_scene_3 = SceneDescription(ObjectPose(translate_3, rotate_3), initAnchor)

        # act
        generator = DoubleAxisSceneGenerator(
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


    def test_generation_of_two_lines_of_scene(self):
        '''
            Should produce two lines of vertical rotation the output should be the 
            same as the two independent runs in @see: SingleAxisSceneGenerator.  
        '''
        # gets beta movements for 0 and 30 !
        beta = GeneratorInterval(0, 30, 30)

        generatorDesc = self.getGeneratorDescription(self.alfa, beta, self.initTranslate)

        initCamera = ObjectPose(self.initTranslate, self.initRotate)
        initAnchor = self.getInitAnchor()



        # setting up expected scenes (line 1)
        x_beta = round(cos(radians(30)), 15) * self.radius
        z_beta = round(sin(radians(30)), 15) * self.radius

        # scene 1 (initial)
        translate_1 = self.initTranslate
        rotate_1 = self.initRotate
        expected_scene_1 = SceneDescription(ObjectPose(translate_1, rotate_1), initAnchor)

        # scene 2
        translate_2 = [0, 5, 0]
        rotate_2 = [radians(60), radians(0), radians(180)]
        expected_scene_2 = SceneDescription(ObjectPose(translate_2, rotate_2), initAnchor)

        # scene 3
        translate_3 = [-5, 0, 0]
        rotate_3 = [radians(60), radians(0), radians(270)]
        expected_scene_3 = SceneDescription(ObjectPose(translate_3, rotate_3), initAnchor)

        # second line of scenes

        # scene 4  
        translate_4 = [x_beta, 0, z_beta]
        rotate_4 = [radians(60), radians(30), radians(90)]
        expected_scene_4 = SceneDescription(ObjectPose(translate_4, rotate_4), initAnchor)

        # scene 5
        translate_5 = [0, x_beta, z_beta]
        rotate_5 = [radians(60), radians(30), radians(180)]
        expected_scene_5 = SceneDescription(ObjectPose(translate_5, rotate_5), initAnchor)

        # scene 6
        translate_6 = [-x_beta, 0, z_beta]
        rotate_6 = [radians(60), radians(30), radians(270)]
        expected_scene_6 = SceneDescription(ObjectPose(translate_6, rotate_6), initAnchor)

        # act
        generator = DoubleAxisSceneGenerator(
                                             generatorDesc=generatorDesc,
                                             initCamera=initCamera,
                                             initAnchor=initAnchor)
        scenes = generator.prepareScenes()


        # verify calling generator intervals
        verify(generatorDesc, atleast=1).alfa
        verify(generatorDesc, atleast=1).beta

        self.assertEqual(6, len(scenes), "Number of scenes generated should be equal to 6")

        # assertions about each scene values
        self.assertEqual(scenes[0], expected_scene_1,
                         self.getDifferMessage(expected_scene_1, scenes[0]))
        self.assertEqual(scenes[1], expected_scene_2,
                         self.getDifferMessage(expected_scene_2, scenes[1]))
        self.assertEqual(scenes[2], expected_scene_3,
                         self.getDifferMessage(expected_scene_3, scenes[2]))

        self.assertEqual(scenes[3], expected_scene_4,
                         self.getDifferMessage(expected_scene_4, scenes[3]))
        self.assertEqual(scenes[4], expected_scene_5,
                         self.getDifferMessage(expected_scene_5, scenes[4]))
        self.assertEqual(scenes[5], expected_scene_6,
                         self.getDifferMessage(expected_scene_6, scenes[5]))

if __name__ == "__main__":
    unittest.main()
