#!/usr/bin/env python3

#--------[ Imports ]-----------------------------------------------------------
import sys
import os
import libtodo as lib
from libtodo import Task

#--------[ GLOBALS ]-----------------------------------------------------------
VERSION     = "0.3"
FILENAME    = "todo.txt"
TODO_DIR    = os.path.dirname(os.path.realpath(sys.argv[0]))
TODO_FILE   = str(TODO_DIR+"/"+FILENAME)

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
    print("--------TODO List--------")
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
    num=int(input("\nWhich group would you like to add this to? "))
    lib.alter_project_by_number(file_data, "add_task", num, temp_task)
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
if len(sys.argv) == 1:
    list_tasks()
    exit()

argument_parser = { "a" : add_task,
                    "d" : delete_task,
                    "f" : finish_task,
                    "h" : Usage,
                    "l" : list_tasks,
                    "u" : unfinish_task,
                    "v" : Version,

                    #Long actions
                    "add"   : add_task,
                    "delete": delete_task,
                    "finish": finish_task,
                    "help"  : Usage,
                    "list"  : list_tasks,
                    "test"  : test_file,
                    "version": Version }

#Check the first argument and default to Usage()
argument_parser.get(sys.argv[1], Usage)()

