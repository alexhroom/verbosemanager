The SimpleVerbose manager
=========================

The SimpleVerbose manager takes away all need to manage the process manually. It is, of course, very inflexible; but it also needs almost no work to function.

Take these processes:

.. code:: python

   def subprocess():
       # subprocess goes here
       
   def process():
       # initialisation goes here
       # process code goes here
       subprocess()
       # more process code goes here
       
To add SimpleVerbose management, simply do the following:

.. code:: python

   @simpleverbose(n_subprocesses=0)
   def subprocess(**verbose):
       # subprocess goes here
       
   @simpleverbose(n_subprocesses=1)
   def process(**verbose):
       # initialisation goes here
       # process code goes here
       subprocess()
       # more process code goes here
       
where ``n_subprocesses`` is of course the number of subprocesses your function goes into. This will return the following:

.. code:: console

   [===============] 100% Complete
   Process completed in [time] seconds.
   Timings per step:
   Process: [time]
   |Subprocess: [time]

This is a little more basic than full verbose management (you can't break processes down into smaller steps) but, again, is very easy (you don't even need to instantiate the manager within your functions!). Like with the ``@verbosedecorator`` decorator, you need to specify verbosity as a ``**kwarg``.

Counting and debugging
----------------------
Like with the regular VerboseManager, you can use the counter with the simple manager by using ``@simplemanager(n_steps, counter=True)``.
