'''
Created on 04-05-2011

Entry point for ALFIRT project. Runs the tests specified in 
command line. Takes command line arguments.

@author: Piotr
'''
from ArgumentParser import ArgumentParser
import sys
from generator.BlenderGenerator import BlenderGenerator
from generator.SceneDescription import SceneDescription

if __name__ == '__main__':

    print "Welcome to ALFIRT project v.0.1 alfa"

    # Get the command line options
    parser = ArgumentParser(sys.argv)

    # Get overall configuration
    configuration = parser.readConfigFile()

    # Get overall input scene for rendering
    scene = parser.readX3DFile()

    generator = BlenderGenerator()
    # Basing on the configuration loop through the possible elements 
    # and generate the images in provided files
    # TODO: add this looping here

    generator.prepareRender(scene)


    # Mark finishing of the runner

    print "Finishing work with ALFIRT project. Bye."

    pass
