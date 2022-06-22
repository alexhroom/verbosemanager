import pytest
from pytest_cases import parametrize
from time import sleep

from verbosemanager import VerboseManager

from tests.expected_values.stdout import EXP_STDOUT


@pytest.fixture
def process():
    """A mock process for testing."""

    def _process(verbose):
        vman = VerboseManager.instance()
        vman.start(2, verbose=verbose)
        sleep(0.01)
        vman.step("Process step 1")
        sleep(0.01)
        vman.step("Process step 2")
        sleep(0.01)
        vman.finish("Process")

    return _process


@pytest.fixture
def bigger_process(process):
    """A mock process that contains process()"""

    def _bigger_process(verbose):
        vman = VerboseManager.instance()
        vman.start(3, verbose=verbose)
        sleep(0.01)
        vman.step("Bigger process step 1")
        sleep(0.01)
        vman.header("Subprocess")
        process(verbose=verbose)
        vman.finish("Bigger process")

    return _bigger_process


@pytest.fixture
def iterative_process():
    """A mock process containing an iterator"""

    def _iterative_process(verbose):
        vman = VerboseManager.instance()
        vman.start(2, verbose=verbose)
        sleep(0.01)
        for i in range(5):
            vman.iterate("Iterator step 1")
            sleep(i * 10e-3)
            vman.iterate("Iterator step 2", iteration_message=f"for iteration {i}")
            sleep(i * 2 * 10e-3)
        vman.finish_iterate()
        vman.step("Finishing")
        vman.finish("Iterative process")

    return _iterative_process


def test_progress():
    """Tests that progress increases and decreases as intended with different methods"""
    vman = VerboseManager.instance()
    vman.start(1, verbose=1)
    assert vman.progress == 0
    vman.header("Header")
    assert vman.progress == 0
    vman.step("Step")
    assert vman.progress == 1
    vman.finish("start, step and header test")
    vman.start(0, verbose=1)
    assert vman.progress == 0
    vman.finish("restart test")


@parametrize("verbose", [1, 2, 3])
@parametrize(
    "func, exp_stdout",
    [(process, "process_stdout"), (bigger_process, "bigger_process_stdout")],
)
def test_stdout(func, exp_stdout, capsys, verbose):
    func(verbose=verbose)
    stdout = capsys.readouterr().out
    assert (EXP_STDOUT[f"{exp_stdout}"])[verbose] in stdout


@parametrize("verbose", [1, 2, 3])
def test_iterate(iterative_process, capsys, verbose):
    iterative_process(verbose=verbose)
    stdout = capsys.readouterr().out
    assert EXP_STDOUT["iterative_process_stdout"][verbose] in stdout
