Repository
~~~~~~~~~~

-  https://github.com/luisholanda/ppm

Features
~~~~~~~~

-  Initialize project folders
-  Install project dependencies without a requirement file
-  Run scripts
-  Start your project script

Commands
~~~~~~~~

#. **Init**

   ::

       ppm {init, i} [-h]

   | Initialize a python module template and a ``pyckage.json`` with
     some basic information that are asked to
   | the user.

   The module template is:

   ::

       ┬ module_name
       │     ├ __init__.py
       │     └ __main__.py
       └ entry_point.py

   Where ``module_name`` and ``entry_point`` values are asked.

#. **Add**

   ::

       ppm {add, a} [-h] [-g] [--add] [<modules>]

   | Install ``<modules>`` in a folder named ``python_modules`` that
     will store all
   | modules that you install with ppm.

   | If the flag ``--add`` is passed, the modules will be added to the
     ``dependencies``
   | field in ``pyckage.json``.

   You can use the ``-g`` flag to install the packages globally.

#. **Remove**

   ::

       ppm {remove, rm} [-h] [-g] <modules>

   Removes a ppm installed package.

   Like the ``add`` command, you can use the ``-g`` flag to remove
   globally installed packages.

#. **Run**

   ::

       ppm run [-h] <script>

   Runs a script that must be specified in ``pyckage.json``.

#. **Start**

   ::

       ppm {start, st} [-h]

   Same thing that the ``run`` command, but only runs the ``start``
   command.