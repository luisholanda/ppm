# Python Package Manager
[![PyPI version](https://badge.fury.io/py/pythonpm.svg)](https://badge.fury.io/py/pythonpm)
[![Build Status](https://travis-ci.org/luisholanda/ppm.svg?branch=master)](https://travis-ci.org/luisholanda/ppm)

Main repository of Python Package Manager (a.k.a ppm), based in npm and yarn from node.

ppm makes project sharing and isolation more easy, using only a `json` file (named `pyckage.json`) to store
the information about your project (name, repository url, dependencies, keywords) like
in Node.js.

It's also create a .ppm.info file to store some information about the modules, 
 like name of egg_info and dist_info.


### Why?

Because the package handling in Python is too damn difficult. pip does a good job installing
packages, but when we want to make a isolated project, we have to deal with `venv` or others
virtual environments utilities and others stuffs.

When I learn node, my first impression about npm was: "This is so much easy that pip".
So I decided to make a program that was equivalent to npm (more close to yarn if you ask me).


### Features

- Initialize project folders
- Install project dependencies without a requirement file
- Run scripts
- Start your project script


### TODO

- Make a version handling for packages installations.
- Make a package search command.
- Make a show command.
- Think in more commands.
- Remove the pip requirement for the `add` command.

#### Obs about subprocess module

**_This is only need if you will create another python instance from your script_**

If you will use `subprocess` module, you will need to pass the env argument when you will create a new subprocess:

```python
import subprocess.Popen
from ppm.utils import set_env

...

env = set_env()
# Any other modifications of environment variables
...

process = subprocess.Popen(..., env=env, ...)
```

If you don't pass the env argument, the `PYTHONPATH` environment variable will not be set correctly in the subprocess.

More precisely, any class/function that create another python instance will need this fix, sadly, I don't know how to
fix this (someone?).

### Commands

1. **Init**

    ```
    ppm {init, i} [-h]
    ``` 
    
    Initialize a python module template and a `pyckage.json` with some basic information that are asked to
    the user.
    
    The module template is:
    
    ```
    ┬ module_name
    │     ├ __init__.py
    │     └ __main__.py 
    └ entry_point.py
    ```
    
    Where `module_name` and `entry_point` values are asked.

2. **Add**

    ```
    ppm {add, a} [-h] [--add] [<modules>]
    ```
    
    Install `<modules>` in a folder named `python_modules` that will store all
    modules that you install with ppm.
    
    If the flag `--add` is passed, the modules will be added to the `dependencies`
    field in `pyckage.json`.
    
3. **Remove**

    ```
    ppm {remove, rm} [-h] <modules>
    ```
    
    Removes a ppm installed package.

4. **Run**

    ```
    ppm run [-h] <script>
    ```

    Runs a script that must be specified in `pyckage.json`.

5. **Start**

    ```
    ppm {start, st} [-h]
    ```

    Same thing that the `run` command, but only runs the `start` command.
