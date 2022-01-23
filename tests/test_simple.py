import pytest
from pytest_cases import parametrize
from time import sleep

from verbosemanager import simpleverbose


# stdout for the fixtures at each verbosity level
process_stdout = {1: "Process complete in 0.01 seconds.",
                  2: ("Process complete in 0.01 seconds.\n"
                      "Timings per step:\n"
                      "Process: 0.01"),
                  3: ('\n\nProcess complete in 0.01 seconds.\n'
                      'Timings per step:\n'
                      'Process: 0.01\n')}

bigger_process_stdout = {1: 'Bigger_Process complete in 0.02 seconds.\n',
                         2: 'Bigger_Process complete in 0.02 seconds.\n'
                            'Timings per step:\n'
                            'Bigger_Process: 0.01\n'
                            '|Process: 0.01\n',
                         3: '\n\r[                    ] 0%  Bigger_Process '
                            '\r[====================] 100%  Process; previous step took 0.01 seconds.  \n'
                            'Bigger_Process complete in 0.02 seconds.\n'
                            'Timings per step:\n'
                            'Bigger_Process: 0.01\n'
                            '|Process: 0.01\n'}


@parametrize("verbose", [1, 2, 3])
@parametrize('func, n_steps, exp_stdout', [("process", 2, process_stdout), ("bigger_process", 3, bigger_process_stdout)])
def test_decorator(verbose, capsys, func, n_steps, exp_stdout):
    """Tests the verbosemanager decorator"""

    @simpleverbose(0)
    def process(**verbose):
        sleep(0.01)

    @simpleverbose(1)
    def bigger_process(**verbose):
        sleep(0.01)
        process(verbose=verbose['verbose'])

    funcs = {
        "process": process,
        "bigger_process": bigger_process
    }

    funcs[func](verbose=verbose)
    stdout = capsys.readouterr().out
    assert exp_stdout[verbose] in stdout
