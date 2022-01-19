import pytest
from pytest_cases import parametrize
from time import sleep

from verbosemanager import verbosify, VerboseManager


@pytest.fixture
def process(**verbose):
    """A mock process for testing."""

    def _process(**verbose):
        verbose_manager = VerboseManager.instance()
        sleep(0.01)
        verbose_manager.step("Process step 1")
        sleep(0.01)
        verbose_manager.step("Process step 2")
        sleep(0.01)

    return _process


@pytest.fixture
def bigger_process(process, **verbose):
    """A mock process that contains process()"""

    def _bigger_process(**verbose):
        verbose_manager = VerboseManager.instance()
        sleep(0.01)
        verbose_manager.step("Bigger process step 1")
        sleep(0.01)
        verbose_manager.header("Subprocess")
        process(verbose=verbose)

    return _bigger_process


# stdout for the fixtures at each verbosity level
process_stdout = {1: "Func complete in 0.03 seconds.",
                  2: ("Func complete in 0.03 seconds.\n"
                      "Timings per step:\n"
                      "Initialising: 0.01\n"
                      "Process step 1: 0.01\n"
                      "Process step 2: 0.01\n"),
                  3: ("\n\r[                    ] 0%  Initialising "
                      "\r[==========          ] 50%  Process step 1; previous step took 0.01 seconds. "
                      "\r[====================] 100%  Process step 2; previous step took 0.01 seconds. \n"
                      "Func complete in 0.03 seconds.\n"
                      "Timings per step:\n"
                      "Initialising: 0.01\n"
                      "Process step 1: 0.01\n"
                      "Process step 2: 0.01\n")}

bigger_process_stdout = {1: 'Func complete in 0.05 seconds.\n',
                         2: 'Func complete in 0.05 seconds.\n'
                            'Timings per step:\n'
                            'Initialising: 0.01\n'
                            'Bigger process step 1: 0.02\n'
                            'Subprocess: \n'
                            'Process step 1: 0.01\n'
                            'Process step 2: 0.01\n',
                         3: '\n\r[                    ] 0%  Initialising '
                            '\r[======              ] 33%  Bigger process step 1; previous step took 0.01 seconds. '
                            '\r[=============       ] 66%  Process step 1; previous step took 0.02 seconds. '
                            '\r[====================] 100%  Process step 2; previous step took 0.01 seconds. \n'
                            'Func complete in 0.05 seconds.\n'
                            'Timings per step:\n'
                            'Initialising: 0.01\n'
                            'Bigger process step 1: 0.02\n'
                            'Subprocess: \n'
                            'Process step 1: 0.01\n'
                            'Process step 2: 0.01\n'}


@parametrize("verbose", [1, 2, 3])
@parametrize('process, n_steps, exp_stdout', [(process, 2, process_stdout), (bigger_process, 3, bigger_process_stdout)])
def test_decorator(verbose, capsys, process, n_steps, exp_stdout):
    """Tests the verbosemanager decorator"""

    @verbosify(n_steps=n_steps)
    def func(fn, **verbose):
        fn(verbose=verbose)

    func(process, verbose=verbose)
    stdout = capsys.readouterr().out
    assert exp_stdout[verbose] in stdout
