'''
Created on 10-05-2011

@author: Piotr
'''
import os
import logging
from configparser import ConfigParser
from generator.data.GeneratorDescription import GeneratorDescription
from generator.data.GeneratorInterval import GeneratorInterval


class ConfigReader(object):
    '''
        Configuration reader for the INI file, reading polar coordinates for image generation, file settings
        additional information for camera object acquisition.
    '''
    defaultAlfaStep = 10
    defaulBetaStep = 10
    defaultRadiusStep = 10

    logger = logging.getLogger()

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


    def __getInputFileName(self, sections):
        if not 'File' in sections:
            # No section files: use all default values
            return GeneratorDescription.defaultInputFileName

        # Get the value from this section
        sectionMap = self.__getSectionMap('File')
        try:
            inputFileName = sectionMap['inputfilename']
        except:
            inputFileName = GeneratorDescription.defaultInputFileName

        return inputFileName


    def readScene(self, fileName):
        '''
            Reads fileName and crates and sets the values.
        @param fileName: path to the fileName which has to be loaded with the configuration 
        @return: GeneratorDescription of the provided file
        '''
        if(fileName == None):
            raise ValueError("The None is not acceptable value for fileName parameter")

        # Try finding this fileName
        if not os.path.exists(fileName):
            raise ValueError("The provided fileName does not exists")

        # Use configuration reader to find this fileName\
        self.logger.info("Reading the configuration file: '" + fileName + "'")

        self.parser = ConfigParser()
        self.parser.read(fileName)

        sections = self.parser.sections()

        # Check for section about polar coordinates
        polarString = 'PolarCoordinates'
        if not polarString in sections:
            raise ValueError("No mandatory polar section in config fileName")


        # Get alfa, beta and radius
        alfa = self.__getInterval(polarString, 'alfastart', 'alfastop', 'alfastep')
        beta = self.__getInterval(polarString, 'betastart', 'betastop', 'betastep')
        radius = self.__getInterval(polarString, 'radiusstart', 'radiusstop', 'radiusstep')

        # Get the fileName name 
        inputFileName = self.__getInputFileName(sections)

        # TODO: change the way it is done here
        inputFormat = GeneratorDescription.defaultInputFormat
        outputFormat = GeneratorDescription.defaultOutputFormat

        gd = GeneratorDescription(alfa, beta, radius, inputFileName, inputFormat, outputFormat)

        return gd
