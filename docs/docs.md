---
layout: default
---

documentation
=============

API reference available [here]({site.baseurl}/docs/api/).

Basic process management
------------------------

For a simple process with no sub-functions (or at least, none that would
require their own verbose handling), `VerboseManager` handles management
like so:

```python
def process(x, y, verbose):
    verbose_manager = VerboseManager.instance()
    verbose_manager.start(2, verbose=verbose)
    # initialisation goes here
    verbose_manager.step("Step 1")
    # step 1 code goes here
    verbose_manager.step("Step 2")
    # step 2 code goes here
    verbose_manager.finish("Process")
```

Note that `VerboseManager` must be instantiated using
`VerboseManager.instance()`; trying to instantiate it using
`VerboseManager()` will throw a runtime error. The reason for this is because `VerboseManager` is a Singleton class - no matter where you instantiate it, it gives you the same single `VerboseManager` object. This is how it manages to track its way through subprocesses etc.

To start the process for `VerboseManager` instance `verbose_manager`, we
use `verbose_manager.start(n_steps, verbose)`. This takes two arguments.
`n_steps` is the number of steps the process involves - see in the
example, this is 2 as the step method is called two times. Sadly, this
must be calculated manually; this is unavoidable, as Python is not a
compiled language. The second parameter is `verbose`, which gives
the verbosity level for the process. The levels are like so:

-   Verbosity 0: no output is given. This is here to save processes from
    having to include a \"`if verbosity>0; verbose_manager.start()`\"
    block - if verbosity is 0, the manager is called and ignored
    entirely.

-   Verbosity 1; no output is given during the process, but when a
    process finishes, the time taken for the whole process is printed,
    and the time taken for a process and all its subprocesses is
    returned as a variable when each process finishes.

-   Verbosity 2; the features of verbosity 1, and additionally and
    additionally at each step a timing is given next to the progress bar
    with how long the previous step took; at the end of the process, a
    list of timings for each step is printed.

-   Verbosity 3; the features of verbosity 1 and 2, and additionally a
    progress bar is given with progress percentage and a message for
    each step.

After starting, we can advance verbose printing for the process using
the method `verbose_manager.step(message)`. This advances the process by
one step, increasing the progress bar and also giving the `message`
parameter as a message next to it. This message should describe what
the current step is doing.

When the process is done, verbose management can be completed using
`verbose_manager.finish(process_name)`. This will end verbose management
for the process (or subprocess). If it is a main process, time taken
will be printed and returned as a variable. If it is a subprocess, time
taken for the subprocess will be returned as a variable. `process_name`
is, of course, a string with the name of the process; final timings will
be printed in the format \"\[process\_name\] complete in \[time\]
seconds.\". Note that if n\_steps was set incorrectly, at this point
`VerboseManager` will throw a warning telling you how many steps it
actually took; if your process takes a fixed number of steps, you could
use this as a quick way of calculating n\_steps.

At verbosity 3, the example given above would print the following at the
end of the process:

```ansiwhite
[===============] 100% Complete
Process completed in [time] seconds.
Timings per step:
Initialisation: [time]
Step 1: [time]
Step 2: [time]
```

Subprocess management
---------------------

If a process involves sub-processes, like so:

```python
def subprocess():
    # subprocess goes here
    
def process():
    # initialisation goes here
    # process code goes here
    subprocess()
    # more process code goes here
```

it is incredibly easy to add the subprocess to `VerboseManager`'s
subprocess management. You simply do the following:

```python
def subprocess():
    verbose_manager = VerboseManager.instance()
    verbose_manager.start(1, verbose=verbose)
    verbose_manager.step("Subprocess step")
    # subprocess goes here
    verbose_manager.finish("Subprocess")
    
def process():
    verbose_manager = VerboseManager.instance()
    verbose_manager.start(3, verbose=verbose)
    # initialisation goes here
    verbose_manager.step("Step 1")
    # step 1 code goes here
    subprocess()
    verbose_manager.step("Step 2")
    # step 2 code goes here
    verbose_manager.finish("Process")
```

that is, to add the subprocess we simply instantiate, start, step and
finish the exact same way as we do in the main process. `VerboseManager`
will recognise that a process is already being managed, and nest the
steps of the subprocess into it.

The only caveat is that `n_steps` in the outermost (main) process must
account for the steps contained in subprocesses. The `n_steps` in the
subprocess is ignored entirely (and would only be used if one was
directly calling the subprocess). This is for a reason; if we added the
subprocess steps to the main process' management as we went, the
progress bar would be incorrect before subprocesses get factored in. At
step 1, it would say we were 50% complete, whereas in fact we have only
done 1 out of 3 steps, so we are in fact 33% complete. This error would
not be corrected until the subprocess starts, leading to weird and
inconsistent output. In fact, if a process had 2 steps and contained a
subprocess with 3 steps, the progress bar would go from 50% to 40% (1/2
to 2/5) when the subprocess starts.

This example would output like so at the end of the process on verbosity
3:

```ansiwhite
[===============] 100% Complete
Process completed in [time] seconds.
Timings per step:
Initialisation: [time]
Step 1: [time]
|Subprocess step: [time]
Step 2: [time]
```

A vertical bar is used to denote the nesting level of subprocesses. As
an example of this, if the subprocess had multiple steps including its
own subprocess, and that sub-subprocess had its own subprocess, it would
nest like so:

```ansiwhite
[===============] 100% Complete
Process completed in [time] seconds.
Timings per step:
Initialisation: [time]
Step 1: [time]
|Subprocess step 1: [time]
||Sub-subprocess step: [time]
|||Sub-sub-subprocess step: [time]
|Subprocess step 2: [time]
Step 2: [time]
```

We can also get timings for a whole subprocess as a return variable,
that is `timings = verbose_manager.finish("Subprocess")`. This will
return the time for the entire subprocess, regardless of how many steps
or sub-subprocesses it goes into. These subprocess timings are stored
simply as a stack; for each new subprocess, its start time is stored,
then retrieved and popped when that subprocess finishes.

The user can also use the method `verbose_manager.header(message)` to
add headers to parts of the final timings list. For example, if we
wanted to add a header to indicate the part of the code that was in the
subprocess, we could add to the previous example:

```python
def process():
    # initialisation etc here
    verbose_manager.step("Step 1")
    # step 1 code here
    verbose_manager.header("Subprocess calculation")
    subprocess()
    # etc...
```

which would print like so:

```ansiwhite
[===============] 100% Complete
Process completed in [time] seconds.
Timings per step:
Initialisation: [time]
Step 1: [time]
Subprocess calculation:
|Subprocess step 1: [time]
||Sub-subprocess step: [time]
|||Sub-sub-subprocess step: [time]
|Subprocess step 2: [time]
Step 2: [time]
```

The @verbosemanager wrapper
-----------------------
The @verbosemanager wrapper is just a shortcut for the `start()` and `finish()` methods. Indeed:

```python
@verbosemanager(1)
def process(**verbose)
  verbose_manager = VerboseManager.instance()
  verbose_manager.step()
  return
```

just does the following:

```python
verbose_manager = VerboseManager.instance()
verbose_manager.start(1, verbose=kwargs(verbose)
process()
verbose_manager.finish(process)
```

This makes it less flexible, as you cannot run anything before starting the verbose management, nor can you change the name of the process given when it finishes (`verbose_manager.finish` here just uses the name of the process it's wrapped around), but it avoids busywork and easily-forgettable finish methods, as well as making your processes look cleaner.

Annoyingly, one still needs to re-instantiate the `VerboseManager` object in each function, as Python scoping does not let a function access objects created in a decorator attached to it.
