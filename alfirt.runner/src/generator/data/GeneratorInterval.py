'''
Created on 02-06-2011

@author: Piotr
'''

class GeneratorInterval(object):
    '''
    Describes the interval in for generating the image.
    @attention: DTO
    '''

    def __init__(self, start, stop, step=0):
        '''
        Constructor.
        @param start: starting point of the interval
        @param stop: stopping point of the interval
        @param step: step used in this interval. 
                     If step is 0 then only one element should be generate equal to start 
        '''
        self.start = start
        self.stop = stop
        self.step = step

    def __str__(self):
        string = "Start: " + self.start + '\n'
        string += "Stop: " + self.stop + '\n'
        string += "Step: " + self.step + '\n'
        return string

    def __eq__(self, o):
        if isinstance(o, GeneratorInterval):
            return o.start == self.start and o.stop == self.stop and o.step == self.step

        return False

    def __ne__(self, o):
        return not self == o

