'''
Created on 11-05-2011

@author: Piotr
'''

class GeneratorDescription(object):
    '''
    Describes the generator settings. Uses back end for polar - euclidian system.
    '''

    def __init__(self, alfa, beta, radius):
        '''
        Constructor.
        @param alfa: alfa parameter of the generator 
        @param beta: beta parameter of the generator
        @param radius: radius parameter of the generator
        '''
        self.alfa = alfa
        self.beta = beta
        self.radius = radius

        pass

