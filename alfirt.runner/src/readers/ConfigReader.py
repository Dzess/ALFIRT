'''
Created on 10-05-2011

@author: Piotr
'''
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

        # Get the file name 
        # TODO: get the reading of this section of the configuration file
        inputFileName = GeneratorDescription.defaultInputFileName
        inputFormat = GeneratorDescription.defaultInputFormat
        outputFormat = GeneratorDescription.defaultOutputFormat

        gd = GeneratorDescription(alfa, beta, radius, inputFileName, inputFormat, outputFormat)

        return gd
