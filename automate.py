import os
import sys
from enum import Enum, unique

######################################################################################
#                                                                                    #
#                                  GLOBALS                                           #
#                                                                                    #
######################################################################################

# All directory paths must end in a slash, and all file paths do not end in a slash

# must be some integer value
MOLECULE = 50

# must be an absolute location path
KTABLE = "somepath"

# must be some integer value
MODELSATATIME = 100

# can be any string
RUNNAME = 'name'

# key must be a string, value must be an integer
PROFILENAMES = {}

# must be an absolute location path 
RUNDICTIONARYPATH = '/home/shellshock/Documents/Repos/BrendansAutomation/'

######################################################################################
#                                                                                    #
#                         CLASSES ENUMS AND STRUCTS                                  #
#                                                                                    #
######################################################################################

# Enum Below verifies and allows Molecules to only be specific numbers
@unique
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
    print("Exiting...")
    exit(0)

def path_failure(path_name):
    print(f"Unable to find path {path_name}")
    program_failure()

# function below verifies that molecule labelled at top is a valid input. 
def verify_molecule(molecule):
    if type(molecule) != int:
        print(f"molecule {molecule} is not an integer, change the value and try again")
        program_failure()
    if molecule not in [mol.value for mol in Molecule]:
        print(f"molecule {molecule} is not a valid value for the molecule.")
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
def read_run_dictionary(run_dictionary_path, current_path):
    # This is the dictionary. key is model # value is Scalar #
    run_dictionary = {}
    
    # If the path exists change directory else failure
    if os.path.exists(run_dictionary_path):
        os.chdir(run_dictionary_path)
    else:
        path_failure(run_dictionary_path)

    # If the path exists get run_dictionary information else failure
    run_dictionary_list = []
    if os.path.exists(run_dictionary_path+'run_dictionary'):
        with open('run_dictionary', 'r') as run_dictionary_file:
            run_dictionary_list = run_dictionary_file.readlines()
    else:
        path_failure(run_dictionary_path+'run_dictionary')

    while run_dictionary_list != []:
        key_values = run_dictionary_list[0].split(' ')
        key = 0
        value = 0.0

        # Verifies that the first value in the run_dictionary is valid. 
        if key_values[0].isdigit():
            key  = int(key_values[0])
        else:
            print(f"Error reading dictionary {key_values[0]} key is not valid input.")
            program_failure()
        
        #removes the newline character from the second string
        key_values[1] = key_values[1].replace('\n', '')

        # Verifies that the second value in run_dictionary is valid
        if key_values[1].replace('.','').isdigit():
            value = float(key_values[1])
        else:
            print(f"Error reading dictionary {key_values[1]} value is not valid input.")
            program_failure()

        run_dictionary[key] = value
        del run_dictionary_list[0]

        
    os.chdir(current_path)
    return run_dictionary

# This function is designed to edit the run_name.apr file
def edit_run_name_apr(run_name_apr_path, scalar, current_path):

    # If Path exists chdir, else path_failure()
    if os.path.exists(run_name_apr_path):
        os.chdir(run_name_apr_path)
    else:
        path_failure(run_name_apr_path)

    file_name = ''
    verify_path = False
    for item in os.listdir(run_name_apr_path):
        if '.apr' in item:
            verify_path = True
            file_name = item
            break

    # Below does action if .apr file is found, else path_failure
    run_name_list = []
    if verify_path:
        with open('run_name.apr', 'r') as run_name_file:
            run_name_list = run_name_file.readlines()
    else:
        path_failure(run_name_apr_path+'*.apr')


    # this is where the editing 'magic' happens
    
    #below subtracts the first number by 1 in the second row. 
    if run_name_list[1][0].isdigit():
        run_name_list[1][0] = str(int(run_name_list[1][0]) - 1) + run_name_list[0][1:]
    else:
        print(f"Unable to convert the first char in string {run_name_list[0]} to int")

    # Deletes rows 3-6
    del run_name_list[2]
    del run_name_list[3]
    del run_name_list[4]
    del run_name_list[5]

    # Below appends the moleule and scalar to the end of file
    run_name_list.append(str(MOLECULE)+' 1 2')
    run_name_list.append(str(scalar)+' 0.5')

    with open('run_name.apr', 'w') as run_name_file:
        run_name_file.write(str(run_name_list))

    os.chdir(current_path)
    
# This function edits the .inp file
def edit_inp(inp_path_name, current_path):
    # Verify path exists, else failure
    if os.path.exists(inp_path_name):
        os.chdir(inp_path_name)
    else:
        path_failure(inp_path_name)
    
    #loop verifies the .inp file is in path, and saves its name
    verify_path = False
    file_name = ''
    for item in os.listdir(inp_path_name):
        if ".inp" in item:
            verify_path = True
            file_name = item
            break
    
    if verify_path:
        rewrite_string = []
        with open(file_name, 'w') as inp_file:
            rewrite_string = inp_file.readlines()
        
        # Changes the 4th line to a 0
        rewrite_string[3] = "0\n"

        # Rewrites the file with a 0 in the 4th spot
        with open(file_name, 'w') as inp_file:
            inp_file.writelines(str.join(rewrite_string))


    else:
        path_failure(inp_path_name+'*.inp')
    
    os.chdir(current_path)

# This function edits the .kls file
def edit_kls(kls_path_name, current_path):
    # Checks if path exists. if it does, chdir else failure
    if os.path.exists(kls_path_name):
        os.chdir(kls_path_name)
    else:
        path_failure(kls_path_name)

    #loop verifies the .kls file is in path, and saves its name
    verify_path = False
    file_name = ''
    for item in os.listdir(kls_path_name):
        if ".kls" in item:
            verify_path = True
            file_name = item
            break
    
    # Checks if path is valid. ifso, append KTABLE to file, else path_failure
    if verify_path:
        with open(file_name, 'a') as kls_file:
            kls_file.write(KTABLE+'\n')
    else:
        path_failure(kls_path_name+'.kls')

    os.chdir(current_path)

# Below removes the aersol.ref and renames aersol.prf to aersol.ref
def aersol_switch(aersol_path, current_path):
    #checks if path exists. if it does chdir, else program_failure()
    if os.path.exists(aersol_path):
        os.chdir(aersol_path)
    else:
        path_failure(aersol_path)
    
    # Checks if aersol.ref is in the path. if it is continue, else program_failure()
    if os.path.exists(aersol_path+"aersol.ref"):

        # Checks if aersol.prf is in path. if it is rm aersol.ref, rename aersol.prf, else program_failure()
        if os.path.exists(aersol_path+"aersol.prf"):
            os.remove("aersol.ref")
            os.rename("aersol.prf", "aersol.ref")
        else:
            path_failure(aersol_path+'aersol.prf')

    else:
        path_failure(aersol_path+'aersol.ref')

    os.chdir(current_path)
    

#Below is the main function, the function that runs it all
def run():
   # below makes sure the molecule is a valid type
   verify_molecule(MOLECULE)

   # stores the current directory value for later use
   current_directory = os.curdir

   # verifies that the RUNDICTIONARYPATH is a string
   if type(RUNDICTIONARYPATH) != str:
       print("RUNDICTIONARYPATH is not of string type, fix it and restart")
       program_failure()

   # gets the run_dictionary
   run_dictionary = read_run_dictionary(RUNDICTIONARYPATH, current_directory)

   for key in run_dictionary:
       full = full_or_forward(key)
       if full:
          print("do a thing")
       else:
          print("do other thing")
   return 



######################################################################################
#                                                                                    #
#                                    START                                           #
#                                                                                    #
######################################################################################
run()