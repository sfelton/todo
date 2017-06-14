#!/usr/bin/env python3

#--------[ Imports ]-----------------------------------------------------------
import sys
import os
import configparser
import getpass

import libtodo as lib
import utilities as util
import colors as c
from libtodo import Task, Project

#--------[ GLOBALS ]-----------------------------------------------------------
VERSION     = "0.6"
CONFIG      = "todo_config.ini"
TODO_DIR    = os.path.dirname(os.path.realpath(sys.argv[0]))

#--------[ Function ]----------------------------------------------------------

#### Usage ##############################################
#                                                       #
# Print usage statement                                 #
#########################################################
def Usage(args):
    print('''
todo - A simple todo list manager to keep a readable todo.txt file

usage: todo [action] [argument]

Actions:
a | add     <task>      Add a task to todo list
f | finish  <task ID>   Finish a task
h | help                Print help
l | list                List tasks
s | sort                Sort finished taks to bottom
  | util    <utility>   Run a TODO Utility
v | version             Print todo version

Utilities:
    test                Tesk todo config and file structure 
    encrypt             Encrypt todo file
    decrypt             Decrypt todo file

''')

#### Version ############################################
#                                                       #
# Print the version number                              #
#########################################################
def Version(args):
    print("todo v{}".format(VERSION))

#### list_tasks #########################################
#                                                       #
# List all tasks in todo list                           #
#########################################################
def list_tasks(args):
    print(c.Bold+"--------TODO List--------"+c.NoC)
    file_data = lib.read_todo_file(TODO_FILE, ENCRYPTED, aes_passphrase)
    lib.list_all_tasks(file_data)

#### add_task ###########################################
#                                                       #
# Add a task to the todo list                           #
#                                                       #
# Check if there is a task in argv[2]. If so, make that #
# that the description. If not, prompt for one.         #
#########################################################
def add_task(args):
    file_data = lib.read_todo_file(TODO_FILE, ENCRYPTED, aes_passphrase)

    if len(sys.argv) == 3:
        desc = sys.argv[2]
    else:
        desc=input("Task description: ")
    temp_task = Task(desc)
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


    lib.write_tasks_to_file(file_data, TODO_FILE, ENCRYPTED, aes_passphrase)

#### delete_task ########################################
#                                                       #
# Delete a task from the todo list                      #
#                                                       #
# Print a numbered list of the all tasks and ask which  #
# one to delete. Then delete that task if it exists     #
#########################################################
def delete_task(args):
    file_data = lib.read_todo_file(TODO_FILE, ENCRYPTED, aes_passphrase)
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

    lib.write_tasks_to_file(file_data, TODO_FILE, ENCRYPTED, aes_passphrase)

#### finish_task ########################################
#                                                       #
# Mark a task as completed                              #
#                                                       #
# Print all the tasks in a numbered list and ask which  #
# one to complete. Complete it if it exists. If the     #
# task is already complete, no error or warning is      #
# printed.                                              #
#########################################################
def finish_task(args):
    file_data = lib.read_todo_file(TODO_FILE, ENCRYPTED, aes_passphrase)
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

    lib.write_tasks_to_file(file_data, TODO_FILE, ENCRYPTED, aes_passphrase)

#### unfinish_task ######################################
#                                                       #
# Mark a task as not completed                          #
#                                                       #
# Print all tasks in numbered list and let the user     #
# choose which one to "unfinish". If the task is marked #
# as not complete, no error or warning is printed.      #
#########################################################
def unfinish_task(args):
    file_data = lib.read_todo_file(TODO_FILE, ENCRYPTED, aes_passphrase)
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

    lib.write_tasks_to_file(file_data, TODO_FILE, ENCRYPTED, aes_passphrase)

#### sort_tasks #########################################
#                                                       #
# Sort the tasks in the todo file to be more readable   #
#                                                       #
# As of right now this will only sort by moving all of  #
# the finished tasksto the bottom of the project.       #
#########################################################
def sort_tasks(args):
    print("I should probably be sorting tasks")
    file_data = lib.read_todo_file(TODO_FILE, ENCRYPTED, aes_passphrase)
    for proj in file_data:
        lib.sort_tasks_in_project(proj)

    lib.list_all_tasks(file_data)

    lib.write_tasks_to_file(file_data, TODO_FILE, ENCRYPTED, aes_passphrase)

#### utilities ##########################################
#                                                       #
# Run a TODO Utility, usually found in utilties.py      #
#                                                       #
# Valid Utilities:                                      #
#  * test     -> test config and todo file structure    #
#  * encrypt  -> encrypt todo file                      #
#  * decrypt  -> decrypt todo file                      #
#########################################################
def utilities(args):
    if len(args) == 0:
        print('''
Utility Usage: todo util <utility>

Utilities:
    test                Tesk todo config and file structure 
    encrypt             Encrypt todo file
    decrypt             Decrypt todo file

''')
        return -2

    retval=0
    if args[0] == "test":
        if not ENCRYPTED:
            retval = util.check_file_structure(TODO_FILE, True)
        else:
            print("[ERRR] This can only be done with decrypted TODO files")
            print("       Please decrypt with `todo util decrypt` first")

    elif args[0] == "encrypt":
        print("\nEncrypting TODO file located at: %s" % TODO_FILE)
        password1 = getpass.getpass("Password: ")
        password2 = getpass.getpass("Repeat Password: ")
        if password1 != password2:
            print("ERROR: Passwords do not match!")
            exit(2)
        else:
            print("\nEncrypting...", end="")
            retval = util.encrypt_file(TODO_FILE, TODO_FILE, password1)
            if retval != 0:
                print("\rERROR: There was a problem encrypting the file")
                exit(2)
            print("Done")

            print("\nEncryption of TODO file was successful.")
            print("Be sure to change the config file to reflect")
            print("'Encryption = True'")

    elif args[0] == "decrypt":
        print("\nDecrypting TODO file located at: %s" % TODO_FILE)
        password = getpass.getpass("Password: ")
        print("\nDecrypting...", end="")

        retval = util.decrypt_file(TODO_FILE, TODO_FILE, password)
        if retval != 0:
            print("\rERROR: There was a problem decrypting the file")
            exit(2)
        print("Done")


        print("\nDecryption of TODO file was successful.")
        print("Be sure to change the config file to reflect")
        print("'Encryption = False'")
    else:
        Usage(args)


#### testtesttest #######################################
#                                                       #
# Test method to test anything we need to               #
#                                                       #
#########################################################
def testtesttest(args):
    print("====TEST METHOD====")
    util.encrypt_file(TODO_FILE, TODO_FILE+".enc", aes_passphrase)
    util.decrypt_file(TODO_FILE+".enc",TODO_FILE+".dec", aes_passphrase)


#--------[ Main ]--------------------------------------------------------------

#Parse through config file
#Check that config file exists and open it
if not os.path.isfile(TODO_DIR+"/"+CONFIG):
    print("[ERROR] Config file, " + CONFIG +", does not exsist")
    exit()
config = configparser.ConfigParser()
config.read(TODO_DIR+"/"+CONFIG)

#Main section of config file
TODO_FILE   = str(TODO_DIR+"/"+config['Main']['file_name'])
ENCRYPTED   = lib.str_to_bool(config['Main']['encryption'])
COLORED     = lib.str_to_bool(config['Main']['colorize_output'])

#Encryption section of the config file
aes_passphrase = ""
if ENCRYPTED:
    if lib.str_to_bool(config['Encryption']['store_password']):
        aes_passphrase = config['Encryption']['password']
    else:
        aes_passphrase = getpass.getpass("Encryption Password: ")

#Colors section of config file
if COLORED:
    LIST_COLORS = lib.get_colors_from_config(config)

#Check for simple case of just running 'todo'
if len(sys.argv) == 1:
    list_tasks(sys.argv)
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
                    "t" : testtesttest,

                    #Long actions
                    "add"   : add_task,
                    "delete": delete_task,
                    "finish": finish_task,
                    "help"  : Usage,
                    "list"  : list_tasks,
                    "sort"  : sort_tasks,
                    "test"  : testtesttest,
                    "util"  : utilities,
                    "version": Version }

#Check the first argument and default to Usage()
argument_parser.get(sys.argv[1], Usage)(sys.argv[2:])

