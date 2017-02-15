# Python Package Manager
[![Build Status](https://travis-ci.org/luisholanda/ppm.svg?branch=master)](https://travis-ci.org/luisholanda/ppm)


##### The client still in development!
Main repository of Python Package Manager (a.k.a ppm), based in npm and yarn from node.

ppm make project sharing and isolation more easy, using only a `json` file (named `pyckage.json`) to store
the information about your project (name, repository url, dependencies, keywords) like
in Node.js.

### Features

- Initialize project folders
- Install project dependencies without a requirement file
- Run scripts
- Start your project

And more is coming!
### Commands

1. **Init**

    ```
    ppm init
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


