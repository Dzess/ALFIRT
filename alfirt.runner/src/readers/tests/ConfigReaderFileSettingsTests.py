'''
Created on Jun 8, 2011

@author: Piotr
'''
import unittest
import os

from readers.ConfigReader import ConfigReader
from generator.data.GeneratorDescription import GeneratorDescription


class ConfigReaderFileSettingsTests(unittest.TestCase):
    '''
        The file setting in the configuration file. Mostly the name of the generated file.
    '''

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

        # Clean Up files
        os.remove(self.fileName)


    def __saveToFile(self, dataString):
        self.fileName = "test_file_with_config_stream"
        with open(self.fileName, 'w') as fileStream:
            fileStream.write(dataString)
            fileStream.close()

        return self.fileName


    def test_passing_the_no_file_setting_results_in_default_values(self):

        configString = """[PolarCoordinates]
        AlfaStart: 20
        AlfaStop: 50
        BetaStart: 100
        BetaStop: 150
        RadiusStart: 10
        RadiusStop: 10
        """
        configString = configString.replace(' ', '')

        fileName = self.__saveToFile(configString)

        reader = ConfigReader()
        settings = reader.readScene(fileName)

        # Assertions go here
        self.assertEqual(GeneratorDescription.defaultInputFileName, settings._inputFileName,
                         "The input file name should be default value")
        self.assertEqual(GeneratorDescription.defaultInputFormat, settings._inputFormat,
                         "The default input format should be .x3d")
        self.assertEqual(GeneratorDescription.defaultOutputFormat, settings.outputFormat,
                          "The default output format should be .bmp")

    def test_passing_good_values_results_in_proper_generator_configuration_settings(self):


        configString = """[PolarCoordinates]
        AlfaStart: 20
        AlfaStop: 50
        BetaStart: 100
        BetaStop: 150
        RadiusStart: 10
        RadiusStop: 10
        [File]
        InputFileName : myFileName
        InputFormat : .collada
        OutputFormat: .jpg
        """

        configString = configString.replace(' ', '')

        fileName = self.__saveToFile(configString)

        reader = ConfigReader()
        settings = reader.readScene(fileName)

        # Assertions go here
        self.assertEqual("myFileName", settings._inputFileName,
                         "The input file name should be 'myFileName'")

if __name__ == '__main__':
    unittest.main()

