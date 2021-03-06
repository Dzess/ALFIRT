'''
Created on 04-05-2011

Entry point for ALFIRT project. Runs the tests specified in 
command line. Takes command line arguments.

@author: Piotr
'''

import sys
import os
import logging

def loggerSetUp():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    logger.info("Welcome to ALFIRT project v.0.2 alfa")
    return logger

def commonsPathSetUp(logger):
    commonNames = os.path.join(__file__, "..", "..", "..", "alfirt.common", "src")
    commonsPath = os.path.abspath(commonNames)

    logger.info("Appending '%s' " % commonsPath)
    sys.path.append(commonsPath)

if __name__ == '__main__':

    logger = loggerSetUp()

    logger.info("Adding to PYTHONPATH requirements from ALFIRT")
    commonsPathSetUp(logger)
    # NOTE: additional path set up here

    # import section
    logger.info("Importing ALFIRT requirements")
    try:
        from generator.BlenderGenerator import BlenderGenerator
        from BlenderRunner import BlenderRunner
        from generator.scene.SceneGenerators import DoubleAxisSceneGenerator
        from readers.ConfigReader import ConfigReader
        from readers.TagReaderX3D import TagReaderX3D
        from ArgumentParser import ArgumentParser
    except ImportError as ie:
        logger.error("The import of ALFIRT requirements was not succesful:\n%s" % ie)
        sys.exit(1)

    # TODO: make this code working with other file formats than x3d only
    configReader = ConfigReader()
    x3dReader = TagReaderX3D()

    # Get the command line options
    parser = ArgumentParser(sys.argv, configReader=configReader, x3dReader=x3dReader)

    # Get overall configuration
    gd = parser.readConfigFile()
    initScene = parser.readX3DFile()

    rootFolder = "runner.output"
    inputFolder = os.path.join(rootFolder, gd.inputFolder).replace('\\', '\\\\').replace('\\\\\ ', '\\\ ')
    outputFolder = os.path.join(rootFolder, gd.outputFolder).replace('\\', '\\\\').replace('\\\\\  ', '\\\ ')


    logger.info("Successfully loaded the configuration file and model file")

    # Overall model mechanics for using the renderer
    # TODO: make those elements plug via factories 
    sg = DoubleAxisSceneGenerator(generatorDesc=gd,
                                  initCamera=initScene.camera,
                                  initAnchor=None)

    rg = BlenderGenerator(generatorDescription=gd,
                          inputFolder=inputFolder,
                          outputFolder=outputFolder)

    # BlenderRunner
    logger.info("Running generator")
    runner = BlenderRunner(generatorDescription=gd,
                           sceneGenerator=sg,
                           renderGenerator=rg,
                           rootFolder=rootFolder,
                           modelFileName=parser.x3dFile)

    runner.execute()

    logger.info("Finishing work with ALFIRT project.")
