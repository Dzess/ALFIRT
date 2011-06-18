'''
Created on 02-06-2011

@author: Piotr
'''

class GeneratorInterval(object):
    '''
    Describes the interval in for generating the image.
    '''

    def __init__(self, start, stop, step):
        '''
        Constructor.
        @param start: starting point of the interval
        @param stop: stopping point of the interval
        @param step: step used in this interval 
        '''
        self.start = start
        self.stop = stop
        self.step = step
