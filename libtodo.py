#!/usr/bin/env python3

from os.path import isfile
from os.path import getsize
from sys import stderr

#--------[ Classes ]-----------------------------------------------------------
class Task(object):

    def __init__(self, desc):
        self.completed   = False
        self.description = desc

    def __str__(self):
        if self.completed:
            return "[X] {}".format(self.description)
        else:
            return "[ ] {}".format(self.description)

class Project(object):

    def __init__(self, n):
        self.tasks=[]
        self.name=n
    
    def add_task(self, t):
        self.tasks.append(t)

#--------[ Methods ]-----------------------------------------------------------
#### read_todo_file #############################################
#                                                               #
# input : filename (string)                                     #
# output: array of projects, each projects contains array       #
#         of tasks                                              #
#                                                               #
# Read the input file line by line. Create a project when one   #
# is found in the todo file. Every task after that will be      #
# placed in the project until another project is encountered.   #
# Push all projects into an array and return that array.        #
#################################################################
def read_todo_file(filename):
    # Check the structure of the file before reading it
    ret = check_file_structure(filename)
    if ret != 0:
        print("ERROR: todo file is not structured properly", file=stderr)
        print("       run 'todo test' to help resolve issues", file =stderr)
        exit(2)

    projects = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            #The first characters of line will tell what it is
            char_key = line[0:2]
            if char_key[0]  == '[':
                temp_task = Task("Placeholder Description")
                temp_task.completed = True if line[1] == 'X' else False
                temp_task.description=line[4:-1]
                temp_project.add_task(temp_task)
            elif char_key == "PR":
                if 'temp_project' in locals():
                  projects.append(temp_project)  
                  del temp_project

                project_desc=line[4:-1]
                temp_project = Project(project_desc)
        #Push the last project onto the array
        projects.append(temp_project)

    return projects

#### write_todo_file ############################################
#                                                               #
# input :                                                       #
# output:                                                       #
#                                                               #
#                                                               #
#################################################################
def write_tasks_to_file(tasks, filename):
    with open(filename, mode="w", encoding='utf-8') as f:
        for t in tasks:
            f.write(t.__str__())
            f.write('\n')

#### list_all_tasks #############################################
#                                                               #
# input : Array of projects to be printed                       #
# output: Print all projects and contained tasks to terminal    #
#                                                               #
# For each project:                                             #
#                   1) Print Project Title                      #
#                   2) Print percent complete                   #
#                   3) Print all contained tasks                #
#################################################################
def list_all_tasks(projects):
    for proj in projects:
        print(proj.name)
        print_tasks(proj.tasks, append=" ")
        print()

#### print_tasks ################################################
#                                                               #
# input : tasks - Array of tasks to print out                   #
#         numbered - Number to start numbering at, -1 for no    #
#                    numbering                                  #
#         append - String to append to each line                #
# output: print each task according to arguments                #
#                                                               #
# This method can be called from any function wanting to print  #
# an array of tasks. The arguments should cover anything needed #
# by calling methods                                            #
#################################################################
def print_tasks(tasks, numbering=-1, append=""):
    for t in tasks:
        print("{}{}".format(append,t))

# NUMBERED: print("({:>2}) {}".format(ctr, t))

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






