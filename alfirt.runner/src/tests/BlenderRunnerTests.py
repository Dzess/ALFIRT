'''
Created on Aug 20, 2011

@author: Piotr
'''
import unittest
import os

from BlenderRunner import BlenderRunner
from mockito.mock import Mock
from generator.BlenderGenerator import BlenderGenerator
from mockito.mockito import when, verify
from mockito import mock
from generator.data.GeneratorDescription import GeneratorDescription
from generator.data.GeneratorInterval import GeneratorInterval
from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose


class BlenderRunnerTests(unittest.TestCase):
    '''
        Integration level test for using the whole set of classes to get 
        the script working and having the file produced
    '''



    def __getGeneratorDescription(self):
        # actually those values are not meant to be used
    # use single value elements
        alfa = GeneratorInterval(5, 5, 1)
        beta = GeneratorInterval(1, 1, 1) # use default step equal to 0
        radius = GeneratorInterval(5, 5)
        gDesc = GeneratorDescription(alfa, beta, radius)
        return gDesc

    def test_running_blender_case_1(self):
        '''
            Test if the blender script is invoked correctly with 
            corresponding runner. Generates SINGLE (one) file for the blender, and
            creates single scene.
        '''
        sGen = Mock()

        # what kind of scenes are to be generated
        camera = ObjectPose([5, 0, 10], [0, 0, 0])
        anchor = ObjectPose([0, 0, 0], [0, 0, 0])

        scene1 = SceneDescription(camera, anchor)
        sceneList = [scene1]
        when(sGen, strict=True).prepareScenes().thenReturn(sceneList)


        #gDesc = self.__getGeneratorDescription()

        # use mock for generator description instead of class
        name = "some_expected_name"

        inputFolder = "foo"
        outputFolder = "bar"

        inputFormat = ".x3d"
        outputFormat = ".bmp"


        gDesc = Mock(GeneratorDescription, strict=True)
        gDesc.inputFolder = inputFolder
        gDesc.outputFolder = outputFolder
        gDesc.inputFormat = inputFormat
        gDesc.outputFormat = outputFormat

        gDesc.inputFileName = name

        bGen = BlenderGenerator(gDesc)

        runner = BlenderRunner(gDesc, sGen, bGen)

        # act
        runner.execute()

        verify(sGen, times=1, atleast=None, atmost=None, between=None)


        input_path = os.path.join(gDesc.inputFolder, name + gDesc.inputFormat)
        output_path = os.path.join(gDesc.outputFolder, name + gDesc.outputFormat)

        print(os.path.abspath(input_path))
        print(os.path.abspath(output_path))

        # assertion about creating file the file should be created in order for rendering
        self.assertTrue(os.path.exists(input_path), "Expected .x3d file could not be found: " + input_path)

        # assertion about generated scene
        self.assertTrue(os.path.exists(output_path), "Expected created .bmp file, could not be found: " + output_path)

if __name__ == "__main__":
    unittest.main()