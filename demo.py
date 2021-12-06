### demo functions
from verbose_manager import VerboseManager
from time import sleep

vmanager = VerboseManager.instance()

def verbosity_0():
    """
    Demo for verbosity 0.
    """
    vmanager.start(15, verbose=0)
    i = 0
    while i < 15:
        i += 1
        # message not used here due to being verbosity 1
        vmanager.step("Iteration i = " + str(i))
        sleep(0.75)
    vmanager.finish("process with verbosity 0")

    print("v=0 done")

def verbosity_1():
    """
    Demo for verbosity 1.
    """
    vmanager.start(15, verbose=1)
    i = 0
    while i < 15:
        i += 1
        # message not used here due to being verbosity 1
        vmanager.step("Iteration i = " + str(i))
        sleep(0.75)
    vmanager.finish("process with verbosity 1")

def verbosity_2():
    """
    Demo for verbosity 2.
    """
    vmanager.start(15, verbose=2)
    i = 0
    while i < 15:
        i += 1
        vmanager.step("Iteration i = " + str(i))
        sleep(0.75)
    vmanager.finish("process with verbosity 2")

def verbosity_3():
    """
    Demo for verbosity 3.
    """
    vmanager.start(15, verbose=3)
    i = 0
    while i < 15:
        i += 1
        vmanager.step("Iteration i = " + str(i))
        sleep(0.75)
    vmanager.finish("process with verbosity 3")

def subprocess(verbose):
    """
    A subprocess for the demo below.
    """
    vmanager = VerboseManager.instance()
    vmanager.start(2, verbose=verbose)
    sleep(1)
    vmanager.step("subprocess step 1")
    sleep(1)
    vmanager.step("subprocess step 2")
    sleep(1)
    vmanager.finish("subprocess")

def run_subprocess():
    """
    Demo for the subprocess alone.
    """
    subprocess(verbose=3)

def verbosity_3_and_subprocess():
    """
    Demo for verbosity 3 featuring the subprocess.
    """
    vmanager.start(15, verbose=3)
    i = 0
    while i < 5:
        i += 1
        sleep(0.75)
        vmanager.step("Iteration i = " + str(i))
        subprocess(verbose=3)
    vmanager.finish("process with verbosity 3 and subprocess")
