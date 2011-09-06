'''
Created on Aug 20, 2011

@author: Piotr
'''
from generator.data.SceneDescription import SceneDescription
from readers.ParserX3D import ParserX3D
from lxml import etree
from mathutils import Quaternion, Euler, Matrix, Vector
from math import sqrt, acos
import string
import logging
import math

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
    logger = logging.getLogger()


    def __init__(self):
        '''
        Constructor
        '''
        self.parser = ParserX3D()

    def __getStringRepresentation(self, elements):
        string = ""
        for element in elements:
            string += str(float(element)) + " "
        string = string[:-1]
        return string

    def __getAxisAngleBasedRotation(self, rotate, translate):

        euler = Euler(rotate)

        self.logger.debug("Injecting rotation: '%s'", str(euler))

        vector_translate = Vector((translate[0], translate[1], translate[2]))

        # actually the translation is also needed to be passed here
        rotate_mtx = Matrix.to_4x4(euler.to_matrix())
        translate_mtx = Matrix.Translation(vector_translate)

        cameraMatrix = translate_mtx * rotate_mtx

        # global matrix rotate (guess it is for world coordinate system rotating)

        mtx = Matrix.Rotation(-(math.pi / 2.0), 4, 'X')
        mtx = mtx * cameraMatrix

        (loc, quat, _) = mtx.decompose()

        # get the values the way that in x3d exporter does
        quat = quat.normalized()

        # some weird stuff
        axises = list(quat.axis.to_tuple())
        angle = quat.angle

        orientation = self.__getStringRepresentation(axises) + " " + str(angle)
        translation = self.__getStringRepresentation(loc)

        return translation, orientation


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

        (final_translate, final_orient) = self.__getAxisAngleBasedRotation(camera.rotate, camera.translate)

        viewpoint.attrib['position'] = final_translate


        viewpoint.attrib['orientation'] = final_orient

        output = str(etree.tostring(tree, pretty_print=True))
        output = output[2:-1]
        output = output.replace("\\n", " ")
        output = output.replace("\\t", " ")
        output = output.replace(string.whitespace, " ")

        return output
