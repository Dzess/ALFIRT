'''
Created on 29-08-2011

@author: Ankhazam
'''
from cPickle import load, dump

class TrainedObject(object):
    '''
    Class representing a trainedObjects
    '''

    def __init__(self, name="ObjectName", surfThreshold=None, orientations=None):
        '''
        Constructor
        
        @param name: Name of the object
        @param surfThreshold: used for training the orientations
        @param orientations: list of  tuples: (@see ImageDescription, surfKeypoints, surfDescriptors, ImagePath)
        '''
        self.name = name
        self.surfThreshold = surfThreshold
        if type(orientations) == type(list()):
            self.orientations = orientations
        else:
            self.orientations = list()
        self.bestMatch = 0
        
    def addOrientation(self, threshold, orientation):
        '''
        Adds new orientation to the list of learnt orientations.
        
        @param threshold: surfThreshold used for aquiring the orientation, must be equal to the objects set threshold.
        @param orientation: (@see ImageDescription, surfKeypoints, surfDescriptors, ImagePath)
        '''
        
        # checks for equality of threshold and on first adding allows setting the threshold        
        if self.surfThreshold is not None:
            if threshold != self.surfThreshold :
                raise ValueError("Surf features extracted with non complaint threshold")
        else :
            if threshold is None:
                raise ValueError("Need to specify the threshold used for training")
            else :
                self.surfThreshold = threshold

        self.orientations.append(orientation)
    
    def load(self, path):
        with open(path) as ofile:
            self.orientations = load(ofile)
            self.bestMatch = 0
        
    def save(self, path):
        with open(path, 'wb') as sfile:
            dump(self.orientations, sfile)
        

