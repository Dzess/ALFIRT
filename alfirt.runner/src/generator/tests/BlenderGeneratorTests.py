'''
Created on Aug 19, 2011

@author: Piotr
'''
import unittest
from generator.data.GeneratorDescription import GeneratorDescription
from generator.BlenderGenerator import BlenderGenerator

class BlenderGeneratorTests(unittest.TestCase):


    def test_simple_printing(self):
        gDesc = GeneratorDescription(inputFileName="token", inputFormat=".x3d", outputFormat=".jpg")
        fileName = "new_file_name"

        bGen = BlenderGenerator(gDesc)
        print(bGen.prepareRender(fileName))


if __name__ == "__main__":
    unittest.main()
