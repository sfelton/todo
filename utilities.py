#!/usr/bin/env python3

#--------[ Imports ]-----------------------------------------------------------
from os.path import isfile
from os.path import getsize

#--------[ Methods ]-----------------------------------------------------------

#### check_file_structure #######################################
#                                                               #
# input:  file path to todo file                                #
# output: 0 if file passes, else the step it failed on          #
#                                                               #
# What to check for:                                            #
#   1) File exists                                              #
#   2) File begins with a project                               #
#   3) All lines are a project or a task                        #
#                                                               #
#################################################################
def check_file_structure(filename, verbose=False):
    if verbose: print("Checking file structure of '{}'...".format(filename))
# 1) Check if file exists
    if verbose: print("\nDoes todo file exist...?")
    if not isfile(filename):
        if verbose:
            ans=input("Would you like to create a new todo file? ")
            if ans == "yes" or ans == "y":
                create_file = open(filename, mode='w')
                create_file.close()
                print("Todo file created at " + filename)
            else:
                return 1
        else:
            return 1
    else:
        if verbose: print("   The file exists")
    #If the file is empty, it passes the test
    if verbose: print("\nIs the file empty...?")
    if getsize(filename) == 0:
        if verbose: print("   The file is empty")
        return 0
    else:
        if verbose: print("   The file is not empty!")
        
# 2) Check if the file begins with a project
    if verbose: print("\nDoes the file begin with a project...?")
    with open(filename, mode = 'r+') as f:
        first_line = f.readline()
        if first_line[0:2] != "PR":
            if verbose:
                print("   The todo file must begin with a project.")
                ans=input("   Would you like create a 'Unsorted' project? ")
                if ans == "yes" or ans =="y":
                    f.seek(0)
                    data = f.read()
                    f.seek(0)
                    f.write("PR  Unsorted\n" + data)
                    print("   'Unsorted' project created")
                else:
                    return 2
            else:
                return 2
        else:
            if verbose: print("   The file begins with a project")

# 3) Check if all lines are valid
    if verbose: print("\nAre all lines valid...?")
    with open(filename, mode='r') as f:
        line_number = 0
        for line in f:
            line_number += 1
            kc = line[0:2]
            if kc!="PR" and kc!="[ " and kc!="[X":
                if verbose:
                    print("   Invalid line: " + str(line_number))
                    print("   Please fix this line")
                    return 3
                else:
                    return 3
        if verbose: print("   All lines are valid")

    if verbose: print("\nFile structure check complete. PASS")
    return 0;

