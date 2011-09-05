'''
Created on 29-08-2011

@author: Ankhazam
'''
from cPickle import load,dump

class TrainedObject(object):
    '''
    classdocs
    '''


    def __init__(self, name="ObjectName", orientation=None):
        '''
        Constructor
        
        @param orientation: (imageDescription, surfFeatures, featuresDescriptors)
        '''
        self.name = name
        self.orientations = [orientation]
        self.bestMatch = 0
        
    def addOrientation(self, orientation):
        '''
        @param orientation: (imageDescription, surfFeatures, featuresDescriptors)
        '''
        self.orientations.append(orientation)
    
    def load(self,path):
        with open(path) as ofile:
            self.orientations = load(ofile)
            self.bestMatch = 0
        
    def save(self,path):
        with open(path,'wb') as sfile:
            dump(self.orientations, sfile)
        