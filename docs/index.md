---
layout: default
---

verbosemanager
==============

verbosemanager is a Python module made for managing verbose output on a complex Python method or function (i.e. one which goes into sub-functions). It allows a process to 'carry' its own verbose management through these sub-functions.

If that answers all your questions, see the 'quick start' guide below. Else, see the 'about' and 'documentation' headings at the top of the page for further information.

Quick start
-----------

1. Ensure you have Python 3.6 or greater.
2. Install the module using pip:
```python
pip3 install verbosemanager
```

3. Import the VerboseManager class into your python script file:
```python
from verbosemanager import VerboseManager
```

4. Get up your favourite process (example process given): 
```python
def subprocess():
    # subprocess goes here
    return something
‎‎‎
def process():
    # initialisation goes here
    # step 1 code goes here
    subprocess()
    # step 2 code goes here
    return something_else
```
5. Add verbosemanager instantiation, start, step, and finish functions:
```python
def subprocess(verbose):
    verbose_manager = VerboseManager.instance()
    verbose_manager.start(n_steps=1, verbose=verbose)
    verbose_manager.step("Subprocess step")
    # subprocess goes here
    verbose_manager.finish("Subprocess")
‎
def process(verbose):
    verbose_manager = VerboseManager.instance()
    verbose_manager.start(n_steps=3, verbose=verbose)
    # initialisation goes here
    verbose_manager.step("Step 1")
    # step 1 code goes here
    subprocess()
    verbose_manager.step("Step 2")
    # step 2 code goes here
    verbose_manager.finish("Process")
```
(where the verbose_manager.start parameters are the number of steps between the start & finish and the verbosity level)

6. You're done! verbosemanager will automatically include the subprocess step in your full process (as long as you account for it in the steps parameter of verbose_manager.start) and users will see something like this after your function finishes:

```ansiwhite
[===============] 100% Complete
Process completed in [time] seconds.
Timings per step:
Initialisation: [time]
Step 1: [time]
|Subprocess step: [time]
Step 2: [time]
```

