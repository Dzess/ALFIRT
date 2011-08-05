'''
Created on 06-05-2011

@author: Piotr
'''
import unittest
from mockito import *


class ArgumentParser(object):
    '''
    Class that specifies how the runner should be worked with. During initializations
    '''
    usageMessage = """Usage: file_with_config x3d_file_with_tags
              """


    def __init__(self, arguments, configReader, x3dReader):
        '''
        Constructor. Creates the instance of the @see: ArgumentParser
        '''

        self.configReader = configReader
        self.x3dReader = x3dReader

        if(arguments == None) or (len(arguments) < 2) :
            raise ValueError(ArgumentParser.usageMessage)

        self.configFile = arguments[0]
        self.x3dFile = arguments[1]

    def readConfigFile(self):
        '''
            Gets the @see: GeneratorDescription from the configuration file.
        '''
        return self.configReader.readFile(self.configFile)

    def readX3DFile(self):
        '''
            Gets the @see: SceneDescription about the saved scene.
            @return: the scene with only anchor and camera filled
        '''
        return self.x3dReader.readFile(self.x3dFile)

#===============================================================================
# UnitTests
#===============================================================================    
class ArgumentParserUnitTests(unittest.TestCase):
    def setUp(self):
        self.fileOne = "config_file_name"
        self.fileTwo = "x3d_file_name"
        self.configReader = mock()
        self.x3dReader = mock()

    def tearDown(self):
        pass

    def test_reading_config_file(self):
        parser = ArgumentParser([self.fileOne, self.fileTwo], self.configReader, self.x3dReader)
        parser.readConfigFile()
        verify(self.configReader).readFile(self.fileOne)

    def test_reading_x3d_file(self):
        parser = ArgumentParser([self.fileOne, self.fileTwo], self.configReader, self.x3dReader)
        parser.readX3DFile()
        verify(self.x3dReader).readFile(self.fileTwo)

    def test_passing_correct_values(self):
        ArgumentParser([self.fileOne, self.fileTwo], self.configReader, self.x3dReader)

    def test_passing_inncorrect_number_of_values_rises_message(self):
        arguments = []
        with self.assertRaises(ValueError) :
            ArgumentParser(arguments, self.configReader, self.x3dReader)

    def test_passing_no_values_results_in_message(self):
        arguments = None
        with self.assertRaises(ValueError):
            ArgumentParser(arguments, self.configReader, self.x3dReader)