#!/usr/bin/env python3

#--------[ Imports ]-----------------------------------------------------------
import sys
import os
import libtodo as lib
from libtodo import Task

#--------[ GLOBALS ]-----------------------------------------------------------
VERSION     = "0.2"
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
    print()

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
    with open(TODO_FILE, mode='a', encoding='utf-8') as f:
        f.write(temp_task.__str__())
        f.write('\n')

#### delete_task ########################################
#                                                       #
# Delete a task from the todo list                      #
#                                                       #
# Print a numbered list of the all tasks and ask which  #
# one to delete. Then delete that task if it exists     #
#########################################################
def delete_task():
    tasks = lib.read_todo_file(TODO_FILE)
    lib.print_numbered_tasks(tasks)
    num=int(input("Which task would you like to delete? "))
    if (num < 1) or (num > len(tasks)):
        print("Task number doesn't exist")
        exit()
    del tasks[num-1]
    lib.write_tasks_to_file(tasks, TODO_FILE)

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
    tasks = lib.read_todo_file(TODO_FILE)
    lib.print_numbered_tasks(tasks)
    num=int(input("Which task did you complete? "))
    if (num < 1) or (num > len(tasks)):
        print("Task number doesn't exist")
        exit()
    tasks[num-1].completed=True
    lib.write_tasks_to_file(tasks, TODO_FILE)

#### unfinish_task ######################################
#                                                       #
# Mark a task as not completed                          #
#                                                       #
# Print all tasks in numbered list and let the user     #
# choose which one to "unfinish". If the task is marked #
# as not complete, no error or warning is printed.      #
#########################################################
def unfinish_task():
    tasks = lib.read_todo_file(TODO_FILE)
    lib.print_numbered_tasks(tasks)
    num=int(input("Which task did you complete? "))
    if (num < 1) or (num > len(tasks)):
        print("Task number doesn't exist")
        exit()
    tasks[num-1].completed=False
    lib.write_tasks_to_file(tasks, TODO_FILE)

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

