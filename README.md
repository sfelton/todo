# TODO

A simple todo list manager that keeps a readable todo.txt file handy.

## Running for the First Time

You can try to run TODO directly after installing it by running `todo`. It will
give you an error saying the 'todo file is not structured not properly'. This
is because there is no file that contains your todo list. To solve this problem
we will run `todo test`. This well run through a series of checks to make sure
that the file containing your todo list is structured in a way that is readable
by TODO. In some cases it will even offer to fix issues for you.

```bash
> todo test
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

## Adding to Your Todo List


