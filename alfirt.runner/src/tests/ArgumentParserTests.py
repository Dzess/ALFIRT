'''
Created on Aug 20, 2011

@author: Piotr
'''
from ArgumentParser import ArgumentParser
import unittest
from mockito import Mock
from mockito import verify

class ArgumentParserUnitTests(unittest.TestCase):
    def setUp(self):
        self.fileOne = "config_file_name"
        self.fileTwo = "x3d_file_name"
        self.configReader = Mock()
        self.x3dReader = Mock()

    def test_reading_config_file(self):
        parser = ArgumentParser(["", self.fileOne, self.fileTwo], self.configReader, self.x3dReader)
        parser.readConfigFile()
        verify(self.configReader).readScene(self.fileOne)

    def test_reading_x3d_file(self):
        parser = ArgumentParser(["", self.fileOne, self.fileTwo], self.configReader, self.x3dReader)
        parser.readX3DFile()
        verify(self.x3dReader).readScene(self.fileTwo)

    def test_passing_correct_values(self):
        ArgumentParser(["", self.fileOne, self.fileTwo], self.configReader, self.x3dReader)

    def test_passing_inncorrect_number_of_values_rises_message(self):
        arguments = []
        with self.assertRaises(ValueError) :
            ArgumentParser(arguments, self.configReader, self.x3dReader)

    def test_passing_no_values_results_in_message(self):
        arguments = None
        with self.assertRaises(ValueError):
            ArgumentParser(arguments, self.configReader, self.x3dReader)

