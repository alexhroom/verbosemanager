import pytest
from pytest_cases import parametrize
from time import sleep

from verbosemanager import verbosedecorator, VerboseManager
from tests.expected_values.stdout import EXP_STDOUT


@parametrize("verbose", [1, 2, 3])
@parametrize(
    "func, n_steps, exp_stdout",
    [("process", 2, "process_stdout"), ("bigger_process", 3, "bigger_process_stdout")],
)
def test_decorator(verbose, capsys, func, n_steps, exp_stdout):
    """Tests the verbosemanager decorator"""

    @verbosedecorator(n_steps=2, name="Process")
    def process(**verbose):
        verbose_manager = VerboseManager.instance()
        sleep(0.01)
        verbose_manager.step("Process step 1")
        sleep(0.01)
        verbose_manager.step("Process step 2")
        sleep(0.01)

    @verbosedecorator(n_steps=3, name="Bigger process")
    def bigger_process(**verbose):
        verbose_manager = VerboseManager.instance()
        sleep(0.01)
        verbose_manager.step("Bigger process step 1")
        sleep(0.01)
        verbose_manager.header("Subprocess")
        process(verbose=verbose["verbose"])

    funcs = {"process": process, "bigger_process": bigger_process}

    funcs[func](verbose=verbose)
    stdout = capsys.readouterr().out
    assert EXP_STDOUT[exp_stdout][verbose] in stdout
