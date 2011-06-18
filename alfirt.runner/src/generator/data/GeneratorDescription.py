'''
Created on 11-05-2011

@author: Piotr
'''

class GeneratorDescription(object):
    '''
    Describes the generator settings. Uses back end for polar - Cartesian system.
    '''
    defaultInputFileName = "input"
    defaultInputFormat = ".x3d"
    defaultOutputFormat = ".bmp"

    def __init__(self, alfa, beta, radius, inputFileName, inputFormat, outputFormat):
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
        self.inputFileName = inputFileName
        self.inputFormat = inputFormat
        self.outputFormat = outputFormat

