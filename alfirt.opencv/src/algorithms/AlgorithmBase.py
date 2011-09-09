'''
Created on Sep 9, 2011

@author: Piotr
'''

class AlgorithmBase(object):
    '''
        Base class for POSE problem algorithms
    '''

    def learn(self, inputFolder):
        raise NotImplementedError("This is abstract method")

    def test(self, inputFolder, outputFolder):
        raise NotImplementedError("This is abstract method")
