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

3. Import the `VerboseManager` class and `@verbosemanager` decorator into your python script file:
```python
from verbosemanager import verbosemanager, VerboseManager
```

4. Open your favourite process (example process given): 
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
5. Add `VerboseManager` instantiation[^1] and step functions, the `**verbose` kwarg to each of your functions, and the `@verbosemanager` decorator:
```python
@verbosemanager(n_steps=1)
def subprocess(**verbose):
    verbose_manager = VerboseManager.instance()
    verbose_manager.step("Subprocess step")
    # subprocess goes here
    return something
‎
@verbosemanager(n_steps=3)
def process(**verbose):
    verbose_manager = VerboseManager.instance()
    # initialisation goes here
    verbose_manager.step("Step 1")
    # step 1 code goes here
    subprocess()
    verbose_manager.step("Step 2")
    # step 2 code goes here
    return something_else
```
(where the `@verbosemanager` parameter, `n_steps`, is the number of step functions called in the process (including those in subfunctions))

6. You're done! `VerboseManager` will automatically include the subprocess step in your full process (as long as you account for it in the steps parameter of `@verbosemanager`) and users will see something like this after your function finishes:

```ansiwhite
[===============] 100% Complete
Process completed in [time] seconds.
Timings per step:
Initialisation: [time]
Step 1: [time]
|Subprocess step: [time]
Step 2: [time]
```

More flexibility is available by directly coding in start and stop functions for your verbose process, but the `@verbosemanager` decorator is a shortcut to access the management functions. See the documentation for details on directly using them.

[^1]: *the instantiation functions are needed so the functions can access the `VerboseManager` class; Python scoping makes this unavoidable, sadly.*
