'''
Created on 06-05-2011

@author: Piotr
'''

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
        return self.configReader.readScene(self.configFile)

    def readX3DFile(self):
        '''
            Gets the @see: SceneDescription about the saved scene.
            @return: the scene with only anchor and camera filled
        '''
        return self.x3dReader.readScene(self.x3dFile)
