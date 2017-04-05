#!/usr/bin/env python3

#--------[ Imports ]-----------------------------------------------------------
import sys
import os
import configparser

import libtodo as lib
import colors as c
from libtodo import Task, Project

#--------[ GLOBALS ]-----------------------------------------------------------
VERSION     = "0.4"
CONFIG      = "todo_config.ini"
TODO_DIR    = os.path.dirname(os.path.realpath(sys.argv[0]))

#--------[ Function ]----------------------------------------------------------

#### Usage ##############################################
#                                                       #
# Print usage statement                                 #
#########################################################
def Usage():
    print('''
todo - A simple todo list manager to keep a readable todo.txt file

usage: todo [action] [argument]

actions:
a | add     <task>      Add a task to todo list
f | finish  <task ID>   Finish a task
h | help                Print help
l | list                List tasks
s | sort                Sort finished taks to bottom
  | test                Tesk todo file structure
v | version             Print todo version
''')

#### Version ############################################
#                                                       #
# Print the version number                              #
#########################################################
def Version():
    print("todo v{}".format(VERSION))

#### list_tasks #########################################
#                                                       #
# List all tasks in todo list                           #
#########################################################
def list_tasks():
    print(c.Bold+"--------TODO List--------"+c.NoC)
    file_data = lib.read_todo_file(TODO_FILE)
    lib.list_all_tasks(file_data)

#### add_task ###########################################
#                                                       #
# Add a task to the todo list                           #
#                                                       #
# Check if there is a task in argv[2]. If so, make that #
# that the description. If not, prompt for one.         #
#########################################################
def add_task():
    if len(sys.argv) == 3:
        desc = sys.argv[2]
    else:
        desc=input("Task description: ")
    temp_task = Task(desc)
    file_data = lib.read_todo_file(TODO_FILE)
    print("--------Projects--------")
    lib.list_all_projects(file_data, 1)
    print("\n(N ) New Project")
    num=input("\nWhich project would you like to add this to? ")
    if num == 'N':
        name=input("\nName of the new project? ")
        temp_proj = Project(name)
        temp_proj.add_task(temp_task)
        file_data.append(temp_proj)
    else:
        lib.alter_project_by_number(file_data, "add_task", int(num), temp_task)
    lib.write_tasks_to_file(file_data, TODO_FILE)

#### delete_task ########################################
#                                                       #
# Delete a task from the todo list                      #
#                                                       #
# Print a numbered list of the all tasks and ask which  #
# one to delete. Then delete that task if it exists     #
#########################################################
def delete_task():
    file_data = lib.read_todo_file(TODO_FILE)
    if (len(sys.argv) > 2) and \
       (sys.argv[2] == "--project" or sys.argv[2] == "-p"):
        print("--------Projects--------")
        lib.list_all_projects(file_data, 1)
        num=int(input("Which project would you like to delete? "))
        if (num < 1) or (num > len(file_data)):
            print("Project number doesn't exist")
            exit()
        lib.alter_project_by_number(file_data, "delete", num)
    else:
        lib.list_all_tasks(file_data, 1)
        num=int(input("Which task would you like to delete? "))
        if (num < 1) or (num > lib.count_all_tasks(file_data)):
            print("Task number doesn't exist")
            exit()
        lib.alter_task_by_number(file_data, "delete", num)

    lib.write_tasks_to_file(file_data, TODO_FILE)

#### finish_task ########################################
#                                                       #
# Mark a task as completed                              #
#                                                       #
# Print all the tasks in a numbered list and ask which  #
# one to complete. Complete it if it exists. If the     #
# task is already complete, no error or warning is      #
# printed.                                              #
#########################################################
def finish_task():
    file_data = lib.read_todo_file(TODO_FILE)
    if (len(sys.argv) > 2) and \
       (sys.argv[2] == "--project" or sys.argv[2] == "-p"):
        print("--------Projects--------")
        lib.list_all_projects(file_data, 1)
        num=int(input("Which project did you complete? "))
        if (num < 1) or (num > len(file_data)):
            print("Project number doesn't exist")
            exit()
        lib.alter_project_by_number(file_data, "finish", num)
    else:
        lib.list_all_tasks(file_data, 1)
        num=int(input("Which task did you complete? "))
        if (num < 1) or (num > lib.count_all_tasks(file_data)):
            print("Task number doesn't exist")
            exit()
        lib.alter_task_by_number(file_data, "finish", num)

    lib.write_tasks_to_file(file_data, TODO_FILE)

#### unfinish_task ######################################
#                                                       #
# Mark a task as not completed                          #
#                                                       #
# Print all tasks in numbered list and let the user     #
# choose which one to "unfinish". If the task is marked #
# as not complete, no error or warning is printed.      #
#########################################################
def unfinish_task():
    file_data = lib.read_todo_file(TODO_FILE)
    if (len(sys.argv) > 2) and \
       (sys.argv[2] == "--project" or sys.argv[2] == "-p"):
        print("--------Projects--------")
        lib.list_all_projects(file_data, 1)
        num=int(input("Which project would you like to un-finish? "))
        if (num < 1) or (num > len(file_data)):
            print("Project number doesn't exist")
            exit()
        lib.alter_project_by_number(file_data, "unfinish", num)
    else:
        lib.list_all_tasks(file_data, 1)
        num=int(input("Which task would you like to un-finish? "))
        if (num < 1) or (num > lib.count_all_tasks(file_data)):
            print("Task number doesn't exist")
            exit()
        lib.alter_task_by_number(file_data, "unfinish", num)

    lib.write_tasks_to_file(file_data, TODO_FILE)

#### sort_tasks #########################################
#                                                       #
# Sort the tasks in the todo file to be more readable   #
#                                                       #
# As of right now this will only sort by moving all of  #
# the finished tasksto the bottom of the project.       #
#########################################################
def sort_tasks():
    print("I should probably be sorting tasks")
    file_data = lib.read_todo_file(TODO_FILE)
    for proj in file_data:
        lib.sort_tasks_in_project(proj)

    lib.list_all_tasks(file_data)

    lib.write_tasks_to_file(file_data, TODO_FILE)

#### test_file ##########################################
#                                                       #
# Test the todo file structure                          #
#                                                       #
# Run the todo file through a series of tests to see if #
# it can be read and manipulated by this program.       #
#########################################################
def test_file():
    retval = lib.check_file_structure(TODO_FILE, True)

#--------[ Main ]--------------------------------------------------------------

#Parse through config file
#Check that config file exists and open it
if not os.path.isfile(TODO_DIR+"/"+CONFIG):
    print("[ERROR] Config file, " + CONFIG +", does not exsist")
    exit()
config = configparser.ConfigParser()
config.read(TODO_DIR+"/"+CONFIG)

#Main section of config file
TODO_FILE = str(TODO_DIR+"/"+config['Main']['file_name'])

#Colors section of config file
if config['Main']['colorize_output'] == "True":
    LIST_COLORS = lib.get_colors_from_config(config)

#Check for simple case of just running 'todo'
if len(sys.argv) == 1:
    list_tasks()
    exit()

#Parse arguments
argument_parser = { "a" : add_task,
                    "d" : delete_task,
                    "f" : finish_task,
                    "h" : Usage,
                    "l" : list_tasks,
                    "s" : sort_tasks,
                    "u" : unfinish_task,
                    "v" : Version,

                    #Long actions
                    "add"   : add_task,
                    "delete": delete_task,
                    "finish": finish_task,
                    "help"  : Usage,
                    "list"  : list_tasks,
                    "sort"  : sort_tasks,
                    "test"  : test_file,
                    "version": Version }

#Check the first argument and default to Usage()
argument_parser.get(sys.argv[1], Usage)()

