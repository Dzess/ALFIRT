'''
Created on 29-08-2011

@author: Ankhazam
'''
from cPickle import load,dump
from test.test_datetime import PicklableFixedOffset
class TrainedObject(object):
    '''
    classdocs
    '''


    def __init__(self, orientation):
        '''
        Constructor
        
        @param orientation: (imageDescription, surfFeatures, featuresDescriptors, matchQuality)
        '''
        self.orientations = [orientation]
        self.bestMatch = 0
        
    def addOrientation(self, orientation):
        '''
        @param orientation: (imageDescription, surfFeatures, featuresDescriptors, matchQuality)
        '''
        self.orientations.append(orientation)
    
    def load(self,path):
        with open(path) as file:
            self.orientations = load(file)
            self.bestMatch = 0
        
    def save(self,path):
        with open(path,'wb') as file:
            dump(self.orientations, file)
        