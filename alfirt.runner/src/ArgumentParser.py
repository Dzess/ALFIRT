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
        pass

    def readConfigFile(self):
        self.configReader.readFile(self.configFile)
        pass

    def readX3DFile(self):
        self.x3dReader.readFile(self.x3dFile)
        pass

#===============================================================================
# UnitTests
#===============================================================================    
class ArgumentParserUnitTests(unittest.TestCase):
    def setUp(self):
        self.fileOne = "config_file_name"
        self.fileTwo = "x3d_file_name"
        self.configReader = mock()
        self.x3dReader = mock()
        pass

    def tearDown(self):
        pass

    def test_reading_config_file(self):
        parser = ArgumentParser([self.fileOne, self.fileTwo], self.configReader, self.x3dReader)
        parser.readConfigFile()
        verify(self.configReader).readFile(self.fileOne)
        pass

    def test_reading_x3d_file(self):
        parser = ArgumentParser([self.fileOne, self.fileTwo], self.configReader, self.x3dReader)
        parser.readX3DFile()
        verify(self.x3dReader).readFile(self.fileTwo)
        pass

    def test_passing_correct_values(self):
        ArgumentParser([self.fileOne, self.fileTwo], self.configReader, self.x3dReader)
        pass

    def test_passing_inncorrect_number_of_values_rises_message(self):
        arguments = []
        with self.assertRaises(ValueError) :
            ArgumentParser(arguments, self.configReader, self.x3dReader)

    def test_passing_no_values_results_in_message(self):
        arguments = None
        with self.assertRaises(ValueError):
            ArgumentParser(arguments, self.configReader, self.x3dReader)


#===============================================================================
# Runner for unittest
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)
