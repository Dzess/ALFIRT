'''
Created on Aug 20, 2011

@author: Piotr
'''
from generator.data.SceneDescription import SceneDescription
from readers.ParserX3D import ParserX3D
from lxml import etree
import string

class SceneInjecterBase(object):
    """
        Abstract class for Scene Injecter
    """

    def injectScene(self, data, scene):
        raise NotImplementedError("This is abstract method")



class SceneInjecterX3D(SceneInjecterBase):
    '''
    Allowing injecting various value into existing string with XML. 
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.parser = ParserX3D()

    def __getStringRepresentation(self, list):
        return "0.0 0.0 0.0"

    def injectScene(self, data, scene):
        '''
        Injects into the specified file scene description values
        @param scene: Object of class @see: SceneDescription
        @param data: String with the data (x3d) in case of this class to be 
        injected into 
        '''
        if not isinstance(data, str):
            raise TypeError("Data expected to be string")

        if not isinstance(scene, SceneDescription):
            raise TypeError("Scene expected to be SceneDescription")

        data = data.encode('ascii', 'ignore')
        tree = etree.fromstring(data)

        (_, _, viewpoint) = self.parser.getViewpointAttributes(tree)
        camera = scene.camera

        # TODO: put math logic for axis angle transformation 
        viewpoint.attrib['position'] = self.__getStringRepresentation(camera.translate)
        viewpoint.attrib['orientation'] = self.__getStringRepresentation(camera.rotate) + " 0.0"

        output = str(etree.tostring(tree, pretty_print=True))
        output = output[2:-1]
        output = output.replace("\\n", " ")
        output = output.replace(string.whitespace, " ")

        return output
