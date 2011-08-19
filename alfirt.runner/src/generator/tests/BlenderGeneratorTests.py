'''
Created on Aug 19, 2011

@author: Piotr
'''
import unittest
from generator.data.GeneratorDescription import GeneratorDescription
from generator.data.SceneDescription import SceneDescription
from generator.BlenderGenerator import BlenderGenerator

class BlenderGeneratorTests(unittest.TestCase):


    def test_simple_printing(self):
        camera = None
        anchor = None

        gDesc = GeneratorDescription(inputFileName="token", inputFormat=".x3d", outputFormat=".jpg")
        sDesc = SceneDescription(camera, anchor)

        bGen = BlenderGenerator(gDesc)
        print(bGen.prepareRender(sDesc))


if __name__ == "__main__":
    unittest.main()
