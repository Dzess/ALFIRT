'''
Created on Jun 8, 2011

@author: Piotr
'''
import unittest
import os

from readers.ConfigReader import ConfigReader

class ConfiReaderPolarCoordinatesTests(unittest.TestCase):
    '''
        Tests all variations of the polar coordinates settings provided
        in the configuration file.
    '''



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

