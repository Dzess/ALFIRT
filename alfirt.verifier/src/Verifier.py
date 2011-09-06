'''
Created on 04-04-2011
Main entry point for ALFIRT Verifier project. Loads the data from  
two files, watches how the metrics are between them. Generates the 
output file with description about differences. 

The file with differences is the .csv file with columns
    file_name; x delta; y delta ; z delta ; p delta ; q delta ; r delta 
    
@attention: 

@author: Piotr Jessa
'''

import sys
import logging
import os

usageMessage = '''
python3 Verifier.py 
    input_directory_with_resulted_image_descriptions
    input_directory_with_original_image_descriptions
    output_directory
               '''

if __name__ == '__main__':

    # lets use root logger
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)

    if len(sys.argv) < 4:
        logger.warn("Please use program with command line options \n%s", usageMessage)
        sys.exit(1)

    logger.info("Checking directories names")
    test_folder = os.path.abspath(sys.argv[1])
    original_folder = os.path.abspath(sys.argv[2])

    output_folder = os.path.abspath(sys.argv[3])

    logger.info("Test   folder: '%s'", test_folder)
    logger.info("Origin folder: '%s'", original_folder)
    logger.info("Output folder: '%s'", output_folder)

    # read from each file out of this folder the structure 
    print("Foo!")
