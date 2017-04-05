#!/usr/bin/env python3

#--------[ Imports ]-----------------------------------------------------------
from os.path import isfile
from os.path import getsize
from sys import stderr
from enum import Enum
import colors

#--------[ Globals ]-----------------------------------------------------------
STATES      = Enum('STATES', 'project_complete\
                              project_in_progress\
                              project_not_started\
                              task_complete\
                              task_in_progress')
COLOR_DICT = dict.fromkeys(STATES, colors.NoC)

#--------[ Classes ]-----------------------------------------------------------
class Task(object):

    def __init__(self, desc):
        self.completed   = False
        self.description = desc

    def __str__(self):
        if self.completed:
            return COLOR_DICT[STATES.task_complete]+"[X] {}".format(self.description)+colors.NoC
        else:
            return "[ ] {}".format(self.description)

    def print_to_file(self):
        if self.completed:
            return "[X] {}".format(self.description)
        else:
            return "[ ] {}".format(self.description)

class Project(object):

    def __init__(self, n):
        self.tasks=[]
        self.name=n
        self.state=STATES.project_not_started
    
    def add_task(self, t):
        self.tasks.append(t)

    def set_state(self, s):
        self.state = s

    def percent_finished(self):
        if len(self.tasks) <= 0:
            return 0
        done = 0
        for t in self.tasks:
            if t.completed:
                done += 1
        return (int(done/len(self.tasks) * 100))

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
        print("[ERROR] todo file is not structured properly", file=stderr)
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
                    if temp_project.percent_finished() == 100:
                        temp_project.set_state(STATES.project_complete)
                    elif temp_project.percent_finished() > 0:
                        temp_project.set_state(STATES.project_in_progress)
                    projects.append(temp_project)  
                    del temp_project

                project_desc=line[4:-1]
                temp_project = Project(project_desc)
        #Push the last project onto the array
        if 'temp_project' in locals():
            if temp_project.percent_finished() == 100:
                temp_project.set_state(STATES.project_complete)
            elif temp_project.percent_finished() > 0:
                temp_project.set_state(STATES.project_in_progress)
            projects.append(temp_project)

    return projects

#### write_todo_file ############################################
#                                                               #
# input : projects - array of projects                          #
#         filename - path to todo file                          #
# output: Writes todo file at the path specified                #
#                                                               #
#################################################################
def write_tasks_to_file(projects, filename):
    with open(filename, mode="w", encoding='utf-8') as f:
        for p in projects:
            f.write("PR  {}".format(p.name))
            f.write('\n')
            for t in p.tasks:
                f.write(t.print_to_file())
                f.write('\n')

#### sort_tasks_in_project  #####################################
#                                                               #
# input : proj - Project to be sorted                           #
#                                                               #
# output: Sort the project so that all finished tasks appear at #
#         at the bottom of the list. There is no return value   #
#                                                               #
#################################################################
def sort_tasks_in_project(proj):
    if proj.percent_finished() != 0 and proj.percent_finished() != 100:
        completed_tasks = []

        index = 0
        for i in range(0, len(proj.tasks)):
            if proj.tasks[index].completed:
                completed_tasks.append(proj.tasks.pop(index))
            else:
                index += 1

        for t in completed_tasks:
            proj.tasks.append(t)


#### list_all_tasks #############################################
#                                                               #
# input : projects - Array of projects to be printed            #
#         num      - Where to start numbering, -1 for no        #
#                    numbering                                  #
# output: Print all projects and contained tasks to terminal    #
#                                                               #
# For each project:                                             #
#                   1) Print Project Title                      #
#                   2) Print percent complete                   #
#                   3) Print all contained tasks                #
#################################################################
def list_all_tasks(projects, num=-1):
    ctr = num
    for proj in projects:
        print(COLOR_DICT[proj.state]+\
              "{} ({}%)".format(proj.name, proj.percent_finished())+\
              colors.NoC)
        if num < 0:
            print_tasks(proj.tasks, append=" ")
        else:
            if len(proj.tasks) > 0:
                print_tasks(proj.tasks, numbering=ctr, append=" ")
                ctr += len(proj.tasks)
        print()

#### list_all_projects ##########################################
#                                                               #
# input : projects - Array of projects to be printed            #
#         num      - Where to start numbering, -1 for no        #
#                    numbering                                  #
# output: No return value                                       #
#                                                               #
# Print out all of the projects contained in the array given.   #
# Do not print out any of the tasks for each project.           #
#################################################################
def list_all_projects(projects, num=-1):
    ctr = num
    for proj in projects:
        if num < 0:
            print(proj.name)
        else:
            print("({:<2}) {}".format(ctr, proj.name))
            ctr += 1

#### print_tasks ################################################
#                                                               #
# input : tasks - Array of tasks to print out                   #
#         numbering - Number to start numbering at, -1 for no    #
#                    numbering                                  #
#         append - String to append to each line                #
# output: print each task according to arguments                #
#                                                               #
# This method can be called from any function wanting to print  #
# an array of tasks. The arguments should cover anything needed #
# by calling methods                                            #
#################################################################
def print_tasks(tasks, numbering=-1, append=""):
    if numbering < 0:
        for t in tasks:
            print("{}{}".format(append,t))
    else:
        ctr = numbering
        for t in tasks:
            print("{}({:>2}) {}".format(append,ctr,t))
            ctr += 1

#### alter_task_by_number #######################################
#                                                               #
# input : projects - array of projects                          #
#         action   - what to do to the task                     #
#         number   - which task to do the action to             #
#         start_num- number to start counting at, usually 1     #
# output: return 0 if successful, non-0 otherwise               #
#                                                               #
# Inteded to be used when the user is prompted to choose a task #
# from a numbered list. This will find the task designated by   #
# the number, and do the chosen action.                         #
# Acceptable Actions: delete, finish, unfinish                  #
#################################################################
def alter_task_by_number(projects, action, number, start_num=1):
    # If number is not the range that this method will check
    if number > (start_num + count_all_tasks(projects) - 1):
        return 1
    ctr = start_num
    for proj in projects:
        local_ctr = 0
        for task in proj.tasks:
            if ctr == number:
                #Found the correct task
                if action == "delete":
                    del proj.tasks[local_ctr]
                    return 0
                elif action == "finish":
                    task.completed = True
                    return 0
                elif action == "unfinish":
                    task.completed = False
                    return 0
                else:
                    return 2
            else:
                local_ctr += 1
                ctr += 1       
    # Shouldn't make it here but just in case
    print("[ERROR] task cannot be found in alter_task_by_number", file=stderr)
    return 3

#### alter_project_by_number ####################################
#                                                               #
# input : projects - array of projects                          #
#         action   - what to do with the group                  #
#         number   - which project to apply action to           #
#         item     - any additional item needed for action      #
#         start_num- number to start counting at, usually 1     #
# output: return 0 if successful, non-0 otherwise               #
#                                                               #
# Alter an entire projects based on its index, usually used     #
# when the user is given a numbered list of projects and gives  #
# the index of their chosen project.                            #
#                                                               #
# Acceptabale Actions: add_task, delete, finish, unfinish       #
#################################################################
def alter_project_by_number(projects, action, number, item=None, start_num=1):
    if (number > start_num + len(projects) - 1) or number < start_num:
        print("Not a valid project index", file=stderr)
        return 1
    curr_proj = projects[number - start_num]
    if action == "add_task":
        if not type(item) is Task:
            print("aler_project_by_nubmer: Given item isn't task!",
                  file=stderr)
            return 2
        projects[number-start_num].add_task(item)
        return 0
    elif action == "delete":
        print()
        print("---- {} ----".format(curr_proj.name))
        print_tasks(curr_proj.tasks)
        ans = input("\nDo you really want to delete '{}'? "\
                .format(curr_proj.name))
        if not (ans == "y" or ans == "yes" or ans == "Y" or ans == "Yes"):
            return 4
        del projects[number - start_num]
        return 0
    elif action == "finish":
        print()
        print("---- {} ----".format(curr_proj.name))
        print_tasks(curr_proj.tasks)
        ans = input("Do you really want to finish '{}'? "\
                .format(curr_proj.name))
        if not (ans == "y" or ans == "yes" or ans == "Y" or ans == "Yes"):
            return 4
        for task in curr_proj.tasks:
            task.completed = True
        return 0
    elif action == "unfinish":
        print()
        print("---- {} ----".format(curr_proj.name))
        print_tasks(curr_proj.tasks)
        ans = input("Do you really want to un-finish '{}'? "\
                .format(curr_proj.name))
        if not (ans == "y" or ans == "yes" or ans == "Y" or ans == "Yes"):
            return 4
        for task in curr_proj.tasks:
            task.completed = False
        return 0
    else:
        print("alter_project_by_number: action no supported", file=stderr)
        return 3

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

#### get_colors_from_config #####################################
#                                                               #
# input : config - A configuration already opend by             #
#                   ConfigParser                                #
#                                                               #
# output: Return a dictionary with the values as the colors and #
#         the keys are the state in which that color should be  #
#         printed.                                              #
#                                                               #
#################################################################
def get_colors_from_config(config):
    #Iterate through Colors section of config at set colors if neccessary
    color_sec = config['Colors']
    for config_state in color_sec:
        for state in STATES:
            if state.name == config_state:
                COLOR_DICT[state] = determine_color(color_sec[config_state])
                break
    return COLOR_DICT

#--------[ Helper Methods ]----------------------------------------------------
#### count_all_tasks ############################################
#                                                               #
# input : projects - array of projects                          #
# output: return total number of tasks contain in those projects#
#                                                               #
# Go through each project and add the length of the tasks array #
# in them.                                                      #
#################################################################
def count_all_tasks(projects):
    num_tasks = 0
    for proj in projects:
        num_tasks += len(proj.tasks)
    return num_tasks

#### determine_color ############################################
#                                                               #
# input : color_str - A string coming from a config file that   #
#                     containst the color text this method will #
#                     determine                                 #
#                                                               #
# output: Return the escape sequece as defined described by     #
#         colors.py to get the desired formated text            #
#                                                               #
#################################################################
def determine_color(color_str):
    return_str = ""
    if color_str == "None":
        return_str = colors.NoC
    elif color_str == "Black":
        return_str = colors.Black
    elif color_str == "Red":
        return_str = colors.Red
    elif color_str == "Green":
        return_str = colors.Green
    elif color_str == "Yellow":
        return_str = colors.Yellow
    elif color_str == "Blue":
        return_str = colors.Blue
    elif color_str == "Purple":
        return_str = colors.Purple
    elif color_str == "Cyan":
        return_str = colors.Cyan
    elif color_str == "White":
        return_str = colors.White
    else:
        print(colors.Red+"[Error] "+colors.NoC+"Format not found")

    return return_str







