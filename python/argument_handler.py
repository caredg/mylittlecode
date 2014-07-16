#!/usr/bin/env python
######################################################
# Author: Edgar Carrera
# ecarrera@cern.ch
# July 12, 2013
# Just the argument handler for any python script
######################################################


import sys
import argparse


#######################################################
def get_arguments():
#######################################################
    """Simple function to parse the arguments using argparse module"""
    
    parser = argparse.ArgumentParser()
    #print help if no arguments are given
    #could be commented out if needed
    if len(sys.argv)==1:
        print ('No arguments found')
        sys.exit(parser.print_help())
        
    #add options for arguments
    #check http://docs.python.org/2/howto/argparse.html
    parser.add_argument("-d", "--dummy", help="dummy option",
                    action="store_true")

    args = parser.parse_args()
    return args


#######################################################
def main():
#######################################################
    """This is just the argument handler for any python script"""
    args = get_arguments()
    if args.dummy:
        print "dummy is True"
        

#######################################################
if __name__ =='__main__':
#######################################################
    sys.exit(main())
    
