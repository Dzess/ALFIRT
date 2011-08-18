'''
Created on 10-05-2011

@author: Piotr
'''
import os

from xml.dom import minidom
from lxml import etree

from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose


class TagReaderX3D(object):
    '''
    Reads the data stream gets the ALFIRT tags from XML document. 
    '''

    namespace = "ALFIRT"

    def __init__(self):
        '''
        Constructor
        '''


    def __getCameraElement(self, xmldoc):
        elements = xmldoc.getElementsByTagName('Viewpoint')

        # Get the first one element from Viewpoint (usually there should be one)
        element = elements[0]

        print("\n")
        print(element.toxml())
        orientation = element.attributes['orientation']
        position = element.attributes['position']

        # Split string by ' ' and get the values
        orientations = orientation.value.split(' ')
        positions = position.value.split(' ')

        translate = []
        translate.append(float(positions[0]))
        translate.append(float(positions[1]))
        translate.append(float(positions[2]))

        rotate = []
        rotate.append(float(orientations[0]))
        rotate.append(float(orientations[1]))
        rotate.append(float(orientations[2]))

        return ObjectPose(translate, rotate)



    def __getPoseOld(self, xmldoc):
        '''
            Uses old XPath library for getting the translation and rotation
        '''
        # Start finding the element about translation and rotation
        # find only the fist element
        rootNode = xmldoc.getElementsByTagName("Scene")[0]
        #context = xpath.XPathContext()
        context = None
        context.namespaces['prefix'] = TagReaderX3D.namespace

        anchor_t_node = context.findnode("//*[@prefix:anchor_translate]", rootNode)
        anchor_r_node = context.findnode("//*[@prefix:anchor_rotate]", rootNode)
        # No anchor element found which is mandatory
        if (anchor_r_node == None) or (anchor_t_node == None):
            raise ValueError("No anchor element found in the file")

        # Read the values from selected nodes
        translations = anchor_t_node.getAttributeNS(TagReaderX3D.namespace, "anchor_translate").split(' ')
        rotations = anchor_r_node.getAttributeNS(TagReaderX3D.namespace, "anchor_rotate").split(' ')
        return translations, rotations

    def __getAttribue(self, tree, name):

        alfirtNamespace = {'prefix' : TagReaderX3D.namespace}
        xpath_expression = "//*[@prefix:" + name + "]"
        nodes = tree.xpath(xpath_expression, namespaces=alfirtNamespace)

        if len(nodes) > 1 :
            raise RuntimeError("Too many ALFIRT tags")

        if len(nodes) == 0 :
            raise RuntimeError("No ALFIRT tag in the passed XML")

        node = nodes[0]
        attributes = node.attrib
        key = '{' + TagReaderX3D.namespace + "}" + name
        values = attributes[key].split(' ')

        return values

    def __getPose(self, tree):
        '''
            Gets tuple (translation, rotation). Uses lxml library
        '''
        translate = self.__getAttribue(tree, "anchor_translate")
        rotate = self.__getAttribue(tree, "anchor_rotate")

        print(translate)
        print(rotate)

        return (translate, rotate)

    def __getAnchorElement(self, xmldoc, tree):

        #translations, rotations = self.__getPoseOld(xmldoc)
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


    def readScene(self, fileName):
        '''
        Reads fileName in .x3d format and returns the data from ALFRT tags.
        @param fileName: the path to the .x3d fileName tagged with ALFIRT attributes. 
        @return: the @see: SceneDescription object with anchor. Camera object is optional.
        
        '''
        if (fileName == None) :
            raise ValueError("The fileName attribute is mandatory")

        if not os.path.exists(fileName):
            raise ValueError("The fileName provided does not exists")

        # using XML broad available library read fileName
        xmldoc = minidom.parse(fileName)
        tree = etree.parse(fileName)

        # Get the anchor element
        anchor = self.__getAnchorElement(xmldoc, tree)

        # Get the camera element
        camera = self.__getCameraElement(xmldoc)

        result = SceneDescription(anchor=anchor, camera=camera)

        return result

