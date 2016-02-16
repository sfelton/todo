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
def read_tasks_from_file(filename):
    if isfile(filename):
        tasks = []
        with open(filename, encoding='utf-8') as f:
            for line in f:
                #The first characters of line will tell what it is
                char_key = line[0:2]
                if char_key[0]  == '[':
                    temp_task = Task("Placeholder Description")
                    temp_task.completed = True if line[1] == 'X' else False
                    temp_task.description=line[4:-1]
                    tasks.append(temp_task)
                elif char_key == "GP":
                    pass
                    #PLACEHOLDER for GROUPS
        return tasks
    else:
        print("No todo file found!")
        print("Creating todo file at " + filename)
        create_file = open(filename, mode="w")
        create_file.close()

def write_tasks_to_file(tasks, filename):
    with open(filename, mode="w", encoding='utf-8') as f:
        for t in tasks:
            f.write(t.__str__())
            f.write('\n')

def print_tasks(tasks):
    print("--------TODO List--------")
    for t in tasks:
        print(t)

def print_numbered_tasks(tasks):
    print("--------TODO List--------")
    ctr = 1;
    for t in tasks:
        print("({:>2}) {}".format(ctr, t))
        ctr += 1

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
        print("   The file is not empty!")
        
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






