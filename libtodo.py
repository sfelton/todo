#!/usr/bin/env python3

from os.path import isfile
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
# output: True/False if file passes test                        #
#                                                               #
# What to check for:                                            #
#   1) File exists
#   2) File begins with a project                               #
#   3) All lines are a project or a task                        #
#                                                               #
#################################################################
def check_file_structure(filename, verbose=False):
    if verbose: print("Checking file structure of '{}'...\n".format(filename))
# 1) Check if file exists
    if verbose: print("Does todo tile exist...?")
    if not isfile(filename):
        print("File '{}' does not exist.".format(filename), file=stderr)
        if verbose:
            ans=input("Would you like to create a new todo file? ")
            if ans == "yes" or ans == "y":
                create_file = open(filename, mode='w')
                create_file.close()
                print("Todo file created at " + filename)
            else:
                exit(1)
    






