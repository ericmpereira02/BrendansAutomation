import os
import sys
from enum import Enum


######################################################################################
#                                                                                    #
#                                  GLOBALS                                           #
#                                                                                    #
######################################################################################
MOLECULE = 50
KTABLE = "somepath"
MODELSATATIME = 100
RUNNAME = "name"
PROFILENAMES

######################################################################################
#                                                                                    #
#                         CLASSES ENUMS AND STRUCTS                                  #
#                                                                                    #
######################################################################################

# Enum Below verifies and allows Molecules to only be specific numbers
class Molecule(Enum):
    MethylCyanide = 50
    NButane       = 78

######################################################################################
#                                                                                    #
#                                 FUNCTIONS                                          #
#                                                                                    #
######################################################################################


# function below is called in the case of a failure, and exits the program
def program_failure():
    printf("Exiting...")
    exit(0)

# function below verifies that molecule labelled at top is a valid input. 
def verify_molecule(molecule):
    if molecule not in Molecule:
        printf("molecule {} is not a valid value for the molecule.", molecule)
        program_failure()
    return

# This function verifies whether a run is a full run or a forward run
def full_or_forward(run):
    isFullRun = False

    #if run is equal to 0 or a centruy run it is considered a full run
    if (run % 100) == 0:
        return True
    
    # If it does not pass the first we check if run is greater than 100. if it is, mod it 
    # by 100 and then we can do the next steps to verify. 
    if (run > 100):
        run = run % 100
    
    #if it is run 30 or run 60 it is a full run, and returns True
    if run == 30 or run == 60:
        return True

    return False 
    
# This function is designed to read in the run_dictionary file, and return a dictionary
def read_run_dictionary(run_dictionary_path):
    run_dictionary = {}
    
# This function is designed to edit the run_name.apr file
def edit_run_name_apr(run_name_apr_path):

# This function is designed to edit the inp file
def edit_inp(inp_path_name):

def edit_kls(kls_path_name):

def aersol_switch(aersol_path):

#Below is the main function, the function that runs it all
def main():
   verify_molecule(MOLECULE)


######################################################################################
#                                                                                    #
#                                    START                                           #
#                                                                                    #
######################################################################################
main()