'''
Created on 10-05-2011

@author: Piotr
'''
import unittest
import os
from ConfigParser import ConfigParser
from generator.GeneratorDescription import GeneratorDescription
from generator.GeneratorInterval import GeneratorInterval


class ConfigReader(object):
    '''
    Configuration reader for the INI file, reading polar coordinates for image generation. 
    '''
    defaultAlfaStep = 10
    defaulBetaStep = 10
    defaultRadiusStep = 10

    def __init__(self):
        '''
        Constructor.
        '''

    def __getSectionMap(self, section):
        '''
        Gets the section of the element and provides to dictionary
        '''
        dict1 = {}
        options = self.parser.options(section)
        for option in options:
            try:
                dict1[option] = self.parser.get(section, option)
                if dict1[option] == -1:
                    raise ValueError("No element in the config file")
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def __getInterval(self, section, start, stop, stepName):
        '''
        Creates interval for section with start stop keys.
        '''
        x = self.__getSectionMap(section)[start]
        y = self.__getSectionMap(section)[stop]

        try:
            z = self.__getSectionMap(section)[stepName]
        except:
            # Add default initialization if there is no step
            if stepName == 'alfastep':
                z = ConfigReader.defaultAlfaStep
            elif stepName == 'betastep':
                z = ConfigReader.defaulBetaStep
            elif stepName == 'radiusstep':
                z = ConfigReader.defaultRadiusStep

        return GeneratorInterval(int(x), int(y), int(z))

    def readFile(self, file):
        '''
        Reads file and crates and sets the values.
        @param file: path to the file which has to be loaded with the configuration 
        '''
        if(file == None):
            raise ValueError("The None is not acceptable value for file parameter")

        # Try finding this file
        if not os.path.exists(file):
            raise ValueError("The provided file does not exists")

        # Use configuration reader to find this file\
        self.parser = ConfigParser()
        self.parser.read(file)

        sections = self.parser.sections()

        # Check for section about polar coordinates
        polarString = 'PolarCoordinates'
        if not polarString in sections:
            raise ValueError("No mandatory polar section in config file")


        # Get alfa, beta and radius
        alfa = self.__getInterval(polarString, 'alfastart', 'alfastop', 'alfastep')
        beta = self.__getInterval(polarString, 'betastart', 'betastop', 'betastep')
        radius = self.__getInterval(polarString, 'radiusstart', 'radiusstop', 'radiusstep')

        gd = GeneratorDescription(alfa, beta, radius)

        return gd


#===============================================================================
#  UnitTests
#===============================================================================
class ConfiReaderUnitTests(unittest.TestCase):



    def __saveToFile(self, fileName, dataINIFormat):
        with open(fileName, 'w') as fileStream:
            fileStream.write(dataINIFormat)
            fileStream.close()

    def setUp(self):

        dataINIFormat = """[PolarCoordinates]
AlfaStart: 20
AlfaStop: 50
BetaStart: 100
BetaStop: 150
RadiusStart: 10
RadiusStop: 10

[Others]
Route: 66 
"""

        dataINIFormatStepped = """[PolarCoordinates]
AlfaStart: 20
AlfaStop: 50
AlfaStep: 1
BetaStart: 100
BetaStop: 150
BetaStep: 2
RadiusStart: 10
RadiusStop: 10
RadiusStep: 3

[Others]
Route: 66 
        """

        # Creating file with no step values
        self.fileName = "test_file_name"
        self.__saveToFile(self.fileName, dataINIFormat)

        self.fileNameWithSteps = "file_with_steps"
        self.__saveToFile(self.fileNameWithSteps, dataINIFormatStepped)
        pass


    def tearDown(self):
        # Removing file after test
        os.remove(self.fileName)
        os.remove(self.fileNameWithSteps)
        pass


    def test_passing_good_values_results_in_data_creaton_default_step(self):
        '''
        Checks when we pass good data, the configReader returns the structure with data
        '''
        # test reading
        configReader = ConfigReader()
        results = configReader.readFile(self.fileName)

        # assert that what was read from file
        self.assertEqual(results.alfa.start, 20, "Alfa start should be 20")
        self.assertEqual(results.alfa.stop, 50, "Alfa stop should be 50")

        self.assertEqual(results.beta.start, 100, "Beta start should be 100")
        self.assertEqual(results.beta.stop, 150, "Beta stop should be 150")

        self.assertEqual(results.radius.start, 10, "Radius start should be 10")
        self.assertEqual(results.radius.stop, 10, "Radius stop should be 10")

        # assertions about the default values
        self.assertEqual(ConfigReader.defaultAlfaStep, results.alfa.step, "The alfa step should be default")
        self.assertEqual(ConfigReader.defaulBetaStep, results.beta.step, "The beta step should be default")
        self.assertEqual(ConfigReader.defaultRadiusStep, results.radius.step, "The radius step should be default")

        pass


    def test_passing_good_values_results_in_data_creation_with_steps(self):
        '''
        Checks when we pass good data, the configReader returns the structure with data
        '''
        # test reading
        configReader = ConfigReader()
        results = configReader.readFile(self.fileNameWithSteps)

        # assert
        self.assertEqual(results.alfa.start, 20, "Alfa start should be 20")
        self.assertEqual(results.alfa.stop, 50, "Alfa stop should be 50")
        self.assertEqual(results.alfa.step, 1, "Alfa step should be 1")

        self.assertEqual(results.beta.start, 100, "Beta start should be 100")
        self.assertEqual(results.beta.stop, 150, "Beta stop should be 150")
        self.assertEqual(results.beta.step, 2, "Beta step should be 2")

        self.assertEqual(results.radius.start, 10, "Radius start should be 10")
        self.assertEqual(results.radius.stop, 10, "Radius stop should be 10")
        self.assertEqual(results.radius.step, 3, "Radius step should be 3")

        pass

    def test_reading_empty_file_results_in_exception(self):
        '''
        Checks if the empty or None conformity file is acceptable 
        '''
        configReader = ConfigReader()
        with self.assertRaises(ValueError):
            configReader.readFile(None)

        with self.assertRaises(ValueError):
            configReader.readFile("non_existing_file")
        pass

#===========================================================================
#  Test runner
#===========================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)

