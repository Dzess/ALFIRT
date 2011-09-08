'''
Created on 04-04-2011
Main entry point for ALFIRT Verifier project. Loads the data from  
two files, watches how the metrics are between them. Generates the 
output file with description about differences. 

The file with differences is the .csv file with columns
    file_name; x delta; y delta ; z delta ; p delta ; q delta ; r delta ; sum_delta
    
@attention: 

@author: Piotr Jessa
'''

import sys
import logging
import os
import csv
import math

headers = ("file_name", "x delta", "y delta" , "z delta" , "p delta" , "q delta" , "r delta" , "sum_delta")

usageMessage = '''
python3 Verifier.py 
    input_folder
    output_directory
               '''

expectedFileName = "expected.imd"
computedFileName = "computed.imd"

def verifyFilesInside(directory, logger):
    '''
        Verifies that how much the two files inside are similar.
        Returns tuple with 7 elements:
        x delta; y delta ; z delta ; p delta ; q delta ; r delta ; sum_delta
    '''
    reader = ImageDescriptionReader()

    expectedFile = os.path.join(directory, expectedFileName)
    computedFile = os.path.join(directory, computedFileName)

    logger.info("Reading expected file '%s'" % expectedFile)
    with open(expectedFile, 'r') as fileStream:
        expected = reader.read(fileStream)

    logger.info("Reading computed file '%s'" % computedFile)
    with open(computedFile, 'r') as fileStream:
        computed = reader.read(fileStream)

    # get reading 
    x_delta = getDelta(expected.x, computed.x)
    y_delta = getDelta(expected.y, computed.y)
    z_delta = getDelta(expected.z, computed.z)

    p_delta = getDeltaRadians(expected.p, computed.p)
    q_delta = getDeltaRadians(expected.q, computed.q)
    r_delta = getDeltaRadians(expected.r, computed.r)

    sum_delta = x_delta + y_delta + z_delta + p_delta + q_delta + r_delta
    return (x_delta, y_delta, z_delta, p_delta, q_delta, r_delta, sum_delta)

def getDelta(a, b):
    '''
        Returns the Minkowski level 1 distance between a,b
    '''
    return round(math.fabs(a - b), 4)

def getDeltaRadians(a, b):
    '''
        Returns absolute value in modulo arithmetic (2*pi)
    '''

    # standarize the a,b
    std_a = a % (2 * math.pi)
    std_b = b % (2 * math.pi)

    diff = math.fabs(std_a - std_b)

    return round(diff, 4)

def saveCSVOutput(resutl_file_name, results, logger):
    logger.info("Saving output into file name '%s'" % resutl_file_name)

    fileName = resutl_file_name + ".csv"
    writer = csv.writer(open(fileName, 'w'), delimiter=';')
    writer.writerow(headers)

    # tuple unpacking
    for r in results:
        inner = []
        inner.append(r[0])
        inner.extend(r[1])
        writer.writerow(inner)


def pathSetUp(logger):
    logger.info("Setting up internal paths to PYTHONPATH")

    commonsPathSetUp(logger)
    # NOTE: add here elements to be used

def commonsPathSetUp(logger):
    commonNames = os.path.join(__file__, "..", "..", "..", "alfirt.common", "src")
    commonsPath = os.path.abspath(commonNames)

    logger.info("Appending '%s' " % commonsPath)
    sys.path.append(commonsPath)


if __name__ == '__main__':

    # lets use root logger
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)

    if len(sys.argv) < 3:
        logger.warn("Please use program with command line options \n%s", usageMessage)
        sys.exit(1)

    logger.info("Welcome to ALFIRT Verifier version 0.2 ")
    pathSetUp(logger)

    try:
        from image.ImageDescriptionReader import ImageDescriptionReader
    except ImportError as importErr:
        logger.error("The ALFIRT requirements could not be imported")
        logger.error(importErr)
        sys.exit(1)

    logger.info("Checking directories names")
    test_folder = os.path.abspath(sys.argv[1])
    output_folder = os.path.abspath(sys.argv[2])

    logger.info("Test   folder: '%s'", test_folder)
    logger.info("Output folder: '%s'", output_folder)

    # creating output folder if does not exists
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # read from each file out of this folder the structure
    results = []
    dirnames = os.listdir(test_folder)
    logger.info("Found '%d' of files inside test folder" % len(dirnames))
    for dirname in dirnames:
        folderPath = os.path.join(test_folder, dirname)
        if os.path.isdir(folderPath):
            logger.info("Verification of object '%s'" % dirname)
            result = verifyFilesInside(folderPath, logger)
            results.append((dirname, result))

    # save the results
    baseName = os.path.basename(test_folder)
    result_file_name = os.path.join(output_folder, baseName)
    saveCSVOutput(result_file_name, results, logger)
    logger.info("Verification finished")
