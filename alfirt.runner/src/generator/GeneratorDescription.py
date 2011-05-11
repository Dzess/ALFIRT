'''
Created on 11-05-2011

@author: Piotr
'''

class GeneratorDescription(object):
    '''
    Describes the generator settings
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

class GeneratorInterval(object):
    '''
    Describes the interval in generation
    '''

    def __init__(self, start, stop):
        '''
        Constructor.
        @param start: starting point of the interval
        @param stop: stopping point of the interval 
        '''
        self.start = start
        self.stop = stop
