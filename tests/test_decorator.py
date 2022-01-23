import pytest
from pytest_cases import parametrize
from time import sleep

from verbosemanager import verbosedecorator, VerboseManager


# stdout for the processes at each verbosity level
process_stdout = {1: "Process complete in 0.03 seconds.",
                  2: ("Process complete in 0.03 seconds.\n"
                      "Timings per step:\n"
                      "Initialising: 0.01\n"
                      "Process step 1: 0.01\n"
                      "Process step 2: 0.01\n"),
                  3: ("\n\r[                    ] 0%  Initialising "
                      "\r[==========          ] 50%  Process step 1; previous step took 0.01 seconds. "
                      "\r[====================] 100%  Process step 2; previous step took 0.01 seconds. \n"
                      "Process complete in 0.03 seconds.\n"
                      "Timings per step:\n"
                      "Initialising: 0.01\n"
                      "Process step 1: 0.01\n"
                      "Process step 2: 0.01\n")}

bigger_process_stdout = {1: 'Bigger_Process complete in 0.05 seconds.\n',
                         2: 'Bigger_Process complete in 0.05 seconds.\n'
                            'Timings per step:\n'
                            'Initialising: 0.01\n'
                            'Bigger process step 1: 0.02\n'
                            'Subprocess: \n'
                            '|Process step 1: 0.01\n'
                            '|Process step 2: 0.01\n',
                         3: '\n\r[                    ] 0%  Initialising '
                            '\r[======              ] 33%  Bigger process step 1; previous step took 0.01 seconds. '
                            '\r[=============       ] 66%  Process step 1; previous step took 0.02 seconds.  '
                            '\r[====================] 100%  Process step 2; previous step took 0.01 seconds.  \n'
                            'Bigger_Process complete in 0.05 seconds.\n'
                            'Timings per step:\n'
                            'Initialising: 0.01\n'
                            'Bigger process step 1: 0.02\n'
                            'Subprocess: \n'
                            '|Process step 1: 0.01\n'
                            '|Process step 2: 0.01\n'}


@parametrize("verbose", [1, 2, 3])
@parametrize('func, n_steps, exp_stdout', [("process", 2, process_stdout), ("bigger_process", 3, bigger_process_stdout)])
def test_decorator(verbose, capsys, func, n_steps, exp_stdout):
    """Tests the verbosemanager decorator"""

    @verbosedecorator(n_steps=2)
    def process(**verbose):
        verbose_manager = VerboseManager.instance()
        sleep(0.01)
        verbose_manager.step("Process step 1")
        sleep(0.01)
        verbose_manager.step("Process step 2")
        sleep(0.01)

    @verbosedecorator(n_steps=3)
    def bigger_process(**verbose):
        verbose_manager = VerboseManager.instance()
        sleep(0.01)
        verbose_manager.step("Bigger process step 1")
        sleep(0.01)
        verbose_manager.header("Subprocess")
        process(verbose=verbose['verbose'])

    funcs = {
        "process": process,
        "bigger_process": bigger_process
    }

    funcs[func](verbose=verbose)
    stdout = capsys.readouterr().out
    assert exp_stdout[verbose] in stdout
