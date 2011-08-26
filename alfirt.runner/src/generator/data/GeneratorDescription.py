'''
Created on 11-05-2011

@author: Piotr
'''
from os.path import abspath
from os.path import join

class GeneratorDescription(object):
    '''
    Describes the generator settings. Uses back end for polar - Cartesian system.
    @attention: DTO
    '''
    defaultInputFileName = "input"
    defaultInputFormat = ".x3d"
    defaultOutputFormat = ".bmp"

    defaultInputFolder = "models"
    defaultOutputFolder = "renders"

    def __init__(self, alfa=None, beta=None, radius=None, inputFileName=defaultInputFileName, inputFormat=defaultInputFormat, outputFormat=defaultOutputFormat):
        '''
        Constructor.
        @param alfa: alfa parameter of the generator 
        @param beta: beta parameter of the generator
        @param radius: radius parameter of the generator
        
        @param inputFileName: file name which will be used to name the images
        @param inputFormat: the format from which the image will be generated
        @param outputFormat: the format in which the image will be generated
        '''

        self.alfa = alfa
        self.beta = beta
        self.radius = radius

        self._inputFileName = inputFileName
        self._inputFormat = inputFormat
        self._outputFormat = outputFormat

        self._inputFolder = GeneratorDescription.defaultInputFolder
        self._outputFolder = GeneratorDescription.defaultOutputFolder

    @property
    def outputFolder(self):
        return self._outputFolder

    @outputFolder.setter
    def outputFolder(self, value):
        self._outputFolder = value

    @property
    def inputFolder(self):
        return self._inputFolder

    @inputFolder.setter
    def inputFolder(self, value):
        self._inputFolder = value
        print(value)

    @property
    def inputFileName(self):
        return self._inputFileName

    @inputFileName.setter
    def inputFileName(self, value):
        self._inputFileName = value

    @property
    def inputFormat(self):
        return self._inputFormat

    @inputFormat.setter
    def inputFormat(self, value):
        self._inputFormat = value

    @property
    def outputFormat(self):
        return self._outputFormat

    @outputFormat.setter
    def outputFormat(self, value):
        self._outputFormat = value


    def getInputFilePath(self):
        name = self._inputFileName + self._inputFormat
        path = join(self._inputFolder, name)
        path = abspath(path)
        return path

    def __str__(self):
        s = "Input File Name: " + self.inputFileName() + "\n"
        s += "Input File Format: " + self.inputFormat() + "\n"
        s += "Format File Format: " + self.outputFormat() + "\n"

        s += "Input Folders :" + self.inputFolder() + "\n"
        s += "Output Folders : " + self.outputFolder() + "\n"
        return s
