#Written by Eric "It Gets Better" Pereira, May 24th, 2021
######################################################################################

import os
import sys
from enum import Enum, unique
from subprocess import Popen, PIPE
import shutil
import time

######################################################################################
#                                                                                    #
#                                  GLOBALS                                           #
#                                                                                    #
######################################################################################

# All directory paths must end in a slash, and all file paths do not end in a slash

#Time at beginning of calculation.
t0=time.time()

# must be some integer value
MOLECULE = 50

print('Currently, your choice of gas number is %s.' % MOLECULE)
dummy=input('Press any key to continue.')

# must be some integer value
MODELSATATIME = 10

# can be any string
RUNNAME = 'fp4_temps'

# must be an absolute location path of NEMESIS directory
NEMESIS = '/Users/brendan/Goddard/Nemesis'

# key must be a string, value must be an integer
PROFILENAMES = {}

# must be an absolute location path for the run_dictionary
RUNDICTIONARYPATH = '/Users/brendan/Goddard/Nemesis/automated/'
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
def associated_full(run):

    # the extended_value is the extended value for numbers > 100 and will
    # always be a factor of 100
    extended_value = 0

    # the deterministic_value is the value used to determine the run
    deterministic_value = 0

    #below runs equations to get accurate deterministic and extended values
    if run > 100:
        deterministic_value = run % 100
        extended_value = run - deterministic_value;
    else:
        deterministic_value = run
    
    # if dv is less than 30, its associated with full run 0 for whatever exteded value is
    if deterministic_value < 30:
        return extended_value
    
    # if dv is less than 60 its associated with full run 30 for whatever extended value is
    if deterministic_value < 60:
        return extended_value + 30

    # in all other cases the dv is associated with full run 60 for whatever extended value is
    return extended_value + 60
    
    
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
    for item in os.listdir(os.curdir):
        if '.apr' in item:
            verify_path = True
            file_name = item
            break

    # Below does action if .apr file is found, else path_failure
    run_name_list = []
    if verify_path:
        with open(RUNNAME+'.apr', 'r') as run_name_file:
            run_name_list = run_name_file.readlines()
    else:
        path_failure(run_name_apr_path+'*.apr')



    line_4_list = run_name_list[3].split(' ')
    line_4_list[0] = str(scalar)
    run_name_list[3] = ' '.join(line_4_list)

    with open(RUNNAME+'.apr', 'w') as run_name_file:
        #run_name_file.write(str(run_name_list))
        for item in run_name_list:
            run_name_file.write(str(item))

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

   #Print the run dictionary and allow user to examine it before beginning.
   print('We are ready to begin.  The forwad model numbers and associated scaling factors used will be:')
   for key in run_dictionary:
       print(key,run_dictionary[key])
   dummy=input('Press any key to continue.')
   
   # Verifies that the NEMESIS directory exists, if not throws and error and fails program. 
   if os.path.exists(NEMESIS):
      print(f'found directory {NEMESIS}')
      os.chdir(NEMESIS)
      print(f'In directory {os.getcwd()}')
   else:
      print(f"The Nemesis folder {NEMESIS} was not found, restart and put in correct value")
      program_failure()

   # for each key in the dictionary do some actions, once the count gets to a specific point
   # create a command for each key, pop, then run automated commands. 
   key_values = []
   a_dictionary = run_dictionary.copy()
   for key in a_dictionary:
       #below gets the associated_full value
       full = associated_full(key)
       destination = shutil.copytree('run'+str(full)+'.0', 'run'+str(key))
       print(f'copied run{full}.0 to run{key}')

       edit_run_name_apr('run'+str(key), run_dictionary[key], NEMESIS)

       #as item gets added it removes from dictoinary and appends to another list for later command. 
       run_dictionary.pop(key)

       key_values.append(key)
       #if the length is equal to modelsatatime or there is no more items left in run_dictionary
       if len(key_values) == MODELSATATIME:
           all_commands = []
           for item in key_values:
               os.chdir(NEMESIS+'/run'+str(item))
               print(f'entering directory {os.getcwd()}')
               command_name = 'Nemesis<'+RUNNAME+'.nam>run'+str(item)+'.log'
               command = Popen(command_name, shell=True, executable="/bin/csh")
               #command.communicate()
               print(f'starting command {command_name}')
               all_commands.append(command)

           for command in all_commands:
              command.wait()
              print(f'finished running command {command}')

           key_values = []
            
           print(f'Finished sequence, moving to the next sequence...')

           os.chdir(NEMESIS)
   if len(key_values) > 0:
      for item in key_values:
         command_name = 'Nemesis<'+RUNNAME+'.nam>run'+str(item)+'.log'
         command = Popen(command_name, shell=True, executable="/bin/csh")
         #command.communicate()
         print(f'starting command {command_name}')
         all_commands.append(command)

      for command in all_commands:
         command.wait()
         print(f'finished running command {command}')

      key_values = []
      
   print(f'Task complete!')
   tf=time.time()
   dt=(tf-t0)/60 #In minutes
   print('Task took %s minutes.' % dt)
   print('Have a good day!  Carpe diem!  Seize the carp!')
    
######################################################################################
#                                                                                    #
#                                    START                                           #
#                                                                                    #
######################################################################################
run()
