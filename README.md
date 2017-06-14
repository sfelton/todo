# TODO

A simple todo list manager that keeps a readable todo.txt file handy.

## Running for the First Time

You can try to run TODO directly after installing it by running `todo`. It will
give you an error saying the 'todo file is not structured not properly'. This
is because there is no file that contains your todo list. To solve this problem
we will run `todo util test`. This well run through a series of checks to make
sure that the file containing your todo list is structured in a way that is
readable by TODO. In some cases it will even offer to fix issues for you.

```bash
$ todo test
Checking file structure of '/Users/user/todo/todo.txt'...

Does todo file exist...?
Would you like to create a new todo file? y
Todo file created at /Users/user/todo/todo.txt

Is the file empty...?
   The file is empty
```

Congratulations, you just created your todo list. Actually all this did was
create an empty file that will soon contain your todo list. By default this
file is called `todo.txt`, this name is customizeable in TODO's configuration.

You can now run `todo` and watch your empty todo list get printed out to the
terminal. Now it's time to start adding projects and tasks to your todo list.

## Using Your Todo List

There are 4 main actions used to interact with your todo list: `add`, `delete`,
`finish`, and `unfinish`. Respectively these add a task, delete a task, mark a
task as finished, and mark a task an not finished.

The easiest way to complete these actions to type `todo <action>` and answer
all of the questions TODO asks.

```bash
$ todo add
Task description: Get feedback
--------Projects--------
(1 ) Project #1 at Work
(2 ) Home

(N ) New Project

Which project would you like to add this to? 1

$ todo
--------TODO List--------
Project #1 at Work (25%)
 [X] Finish research
 [ ] Finish report
 [ ] Submit report
 [ ] Get feedback

Home (0%)
  [ ] Take the trash out
  [ ] Walk the dog
```

## Encryption

TODO provides the ability to encrypt your TODO file to ensure that only the
people with the encryption password will be able to read your todo list.
Setting up encryption consists of initially encrypting the file and changing
the configuration so TODO knows that it is now dealing with an encrypted file.

### Encrypting your TODO file

This is as easy as running `todo util encrypt`. It will ask you for a password,
don't forget it or else you won't be able to decrypt your todo list.

```bash
$ todo util encrypt

Encrypting TODO file located at: /Users/user/todo/todo.txt
Password:
Repeat Password:

Encrypting...Done

Encryption of TODO file was successful.
Be sure to change the config file to reflect
'Encryption = True'

$ cat todo.txt | xxd
00000000: 44e3 8d48 a997 3f0e e6c6 beaf 1778 24c4  D..H..?......x$.
00000010: 63d2 4ac0 eb03 add2 091c 0a19 c453 092a  c.J..........S.*
00000020: 1315 d396 7bd4 2027 4ecc c6ad bc19 611b  ....{. 'N.....a.
00000030: 98cb 08b2 6c71 33b4 4af7 f397 647e 05dd  ....lq3.J...d~..
00000040: 50cd 474b 5450 bd16 ac11 e091 7e50 6d83  P.GKTP......~Pm.
00000050: d796 9185 fb27 88aa 5673 2e41 7f9d bd65  .....'..Vs.A...e
00000060: 9a76 0a5a 26b5 60fe 11a9 2969 b15f 5ba6  .v.Z&.`...)i._[.
00000070: dd7b a1ea 692f 30d2 971b d2c8 0816 ca3f  .{..i/0........?
00000080: b430 48e5 d74f 2e8c ea67 76eb 025f bcb3  .0H..O...gv.._..
00000090: 2d2e dd5d 13f9 d489 16bb 9f3d 7b57 4352  -..].......={WCR
000000a0: 5fb9 a3b9 bafa 8dc7 d757 b38b 2d9f 9def  _........W..-...
000000b0: 84a4 9d3c ff77 b1ce d09e b806 442b 8d5c  ...<.w......D+.\
```

### Configuring TODO for encryption

All of the configuration option for TODO can be found in the `todo_config.ini`
file. After the TODO file is encrypted that are a few lines in the file that
need to be changed. 

The first is just to turn on Encryption:
```bash
Encryption  = True
```

Congratulations, you are now set up to interact with an encrypted TODO file.
There are more configurable options under the `[Encryption]` section of the
config file. Feel free to explore those options.
