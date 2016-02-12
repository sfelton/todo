#!/usr/bin/env python3

import sys
import os
import libtodo as lib
from libtodo import Task

#--------[ GLOBALS ]-----------------------------------------------------------
VERSION     = "0.1"
FILENAME    = "todo.txt"
TODO_DIR    = os.path.dirname(os.path.realpath(sys.argv[0]))
TODO_FILE   = str(TODO_DIR+"/"+FILENAME)

def Usage():
    print('''
todo - A simple todo list manager to keep a readable todo.txt file

usage: todo [action] [argument]

actions:
a | add     <task>      Add a task to todo list
f | finish  <task ID>   Finish a task
h | help                Print help
l | list                List tasks
v | version             Print todo version
''')

def Version():
    print("todo v{}".format(VERSION))

def add_task():
    desc=input("Task description: ")
    temp_task = Task(desc)
    with open(TODO_FILE, mode='a', encoding='utf-8') as f:
        f.write(temp_task.__str__())
        f.write('\n')

def delete_task():
    tasks = lib.read_tasks_from_file(TODO_FILE)
    lib.print_numbered_tasks(tasks)
    num=int(input("Which task would you like to delete? "))
    if (num < 1) or (num > len(tasks)):
        print("Task number doesn't exist")
        exit()
    del tasks[num-1]
    lib.write_tasks_to_file(tasks, TODO_FILE)

def finish_task():
    tasks = lib.read_tasks_from_file(TODO_FILE)
    lib.print_numbered_tasks(tasks)
    num=int(input("Which task did you complete? "))
    if (num < 1) or (num > len(tasks)):
        print("Task number doesn't exist")
        exit()
    tasks[num-1].completed=True
    lib.write_tasks_to_file(tasks, TODO_FILE)

def unfinish_task():
    tasks = lib.read_tasks_from_file(TODO_FILE)
    lib.print_numbered_tasks(tasks)
    num=int(input("Which task did you complete? "))
    if (num < 1) or (num > len(tasks)):
        print("Task number doesn't exist")
        exit()
    tasks[num-1].completed=False
    lib.write_tasks_to_file(tasks, TODO_FILE)

def list_tasks():
    tasks = lib.read_tasks_from_file(TODO_FILE)
    lib.print_tasks(tasks)


"""
Parse through arguments
"""
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
                    "version": Version }

#Check the first argument and default to Usage()
argument_parser.get(sys.argv[1], Usage)()

