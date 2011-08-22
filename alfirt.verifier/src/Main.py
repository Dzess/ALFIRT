'''
Created on 04-04-2011
Main entry point for ALFIRT Verifier project. Loads the data from  
two files, watches how the metrics are between them. Generates the 
output file with description about differences.
 

@author: Piotr Jessa
'''

import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage message should be printed here")
        sys.exit(1)

    #TODO write reading line from system argv, and invoking good classes for that
