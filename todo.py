#!/usr/bin/env python3

import sys


def Usage():
    print('''
todo - A simple todo list manager to keep a readable todo.txt file

usage: todo [action] [argument]

actions:
a | add     <task>      Add a task to todo list
f | finish  <task ID>   Finish a tak
h | help                Print help
l | list                List tasks
v | version             Print todo version
''')

def Version():
    print("Version")

def add_task():
    print("Add task")

def finish_task():
    print("Finish task")

def list_tasks():
    print("List Tasks")



"""
Parse through arguments
"""
if len(sys.argv) == 1:
    list_tasks()
    exit()

argument_parser = { "a" : add_task,
                    "f" : finish_task,
                    "h" : Usage,
                    "l" : list_tasks,
                    "v" : Version,

                    #Long actions
                    "add"   : add_task,
                    "finish": finish_task,
                    "help"  : Usage,
                    "list"  : list_tasks,
                    "version": Version }

argument_parser[sys.argv[1]]()

