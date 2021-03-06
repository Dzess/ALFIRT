'''
Created on Aug 22, 2011

@author: Piotr
'''

import logging
from lxml import etree
from generator.data.ObjectPose import ObjectPose

import math
from mathutils import Quaternion, Euler, Matrix, Vector

class ParserX3D(object):
    '''
        Helper class for X3D document parsings

    '''
    defaultNamespace = "ALFIRT"
    logger = logging.getLogger()

    def __init__(self, namespace=defaultNamespace):
        '''
        @param namespace: string representing the namespae to be used
        '''
        if not isinstance(namespace, str):
            raise TypeError("namespace parameter expected to be string")

        self.alfirtNamespace = {'prefix' : namespace}

    def __getPose(self, tree):
        '''
            Gets tuple (translation, rotation). Uses lxml library
        '''
        translate = self.__getAttribue(tree, "anchor_translate")
        rotate = self.__getAttribue(tree, "anchor_rotate")

        return (translate, rotate)


    def __getAttribue(self, tree, name):
        '''
            Gets values for the given attrubute
        '''

        xpath_expression = "//*[@prefix:" + name + "]"
        nodes = tree.xpath(xpath_expression, namespaces=self.alfirtNamespace)

        if len(nodes) > 1 :
            raise RuntimeError("Too many ALFIRT tags")

        if len(nodes) == 0 :
            raise RuntimeError("No ALFIRT tag in the passed XML")

        node = nodes[0]
        attributes = node.attrib
        key = '{' + ParserX3D.defaultNamespace + "}" + name
        values = attributes[key].split(' ')

        return values

    def getViewpointAttributes(self, tree):
        '''
            Searches XML with XPATH for Viewpoint element. 
            @return: tuple with position and orientation string
                     the third element on tuple is viewpoint lxml objectified element
        '''

        viewpoint_elements = tree.xpath("//Viewpoint")
        if len(viewpoint_elements) == 0:
            raise RuntimeError("No Viewpoint found")
        if len(viewpoint_elements) > 1:
            raise RuntimeError("Too many Viewpoints found")

        viewpoint = viewpoint_elements[0]

        position = viewpoint.attrib['position']
        orientation = viewpoint.attrib['orientation']

        return (position, orientation, viewpoint)

    def __getAxisAngleFromEulerAngles(self, rotate, translate):
        # TODO: implement this code from export.x3d
        pass

    def __getEulerAnglesFromAxisAngle(self, rotate, translate):

        mtx = Matrix.Translation(Vector(translate)) * self.__translateRotation(rotate)
        mtx = Matrix.Rotation(math.pi / 2.0, 4, 'X') * mtx
        euler = mtx.to_euler()
        return [euler.x, euler.y, euler.z]

    def __translateRotation(self, rot):
        ''' axis, angle '''
        return Matrix.Rotation(rot[3], 4, Vector(rot[:3]))

    def getCameraElement(self, tree):

        (position, orientation, _) = self.getViewpointAttributes(tree)

        self.logger.debug("Camera position translate: '" + str(position) + "'")
        self.logger.debug("Camera position rotation: '" + str(orientation) + "'")

        # Split string by ' ' and get the values
        orientations = orientation.split(' ')
        positions = position.split(' ')

        # element are reversed in the x3d from blender
        translate = []
        translate.append(float(positions[0]))
        translate.append(float(positions[2]))
        translate.append(float(positions[1]))

        rotate = []
        rotate.append(float(orientations[0]))
        rotate.append(float(orientations[1]))
        rotate.append(float(orientations[2]))
        rotate.append(float(orientations[3]))

        rotate_euler = self.__getEulerAnglesFromAxisAngle(rotate, translate)
        return ObjectPose(translate, rotate_euler)

    def getAnchorElement(self, tree):

        translations, rotations = self.__getPose(tree)

        translate = []
        rotate = []

        translate.append(float(translations[0]))
        translate.append(float(translations[1]))
        translate.append(float(translations[2]))

        rotate.append(float(rotations[0]))
        rotate.append(float(rotations[1]))
        rotate.append(float(rotations[2]))

        return ObjectPose(translate, rotate)

