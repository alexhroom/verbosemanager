import pytest
from pytest_cases import parametrize
from time import sleep

from verbosemanager import VerboseManager


@pytest.fixture
def process():
    """A mock process for testing."""

    def _process(verbose):
        vman = VerboseManager.instance(counter=True)
        vman.start(2, verbose=verbose)
        sleep(0.01)
        vman.step("Process step 1")
        sleep(0.01)
        vman.step("Process step 2")
        sleep(0.01)
        results = vman.finish("Process")
        return results

    return _process


@pytest.fixture
def bigger_process(process):
    """A mock process that contains process()"""

    def _bigger_process(verbose):
        vman = VerboseManager.instance(counter=True)
        vman.start(3, verbose=verbose)
        sleep(0.01)
        vman.step("Bigger process step 1")
        sleep(0.01)
        vman.header("Subprocess")
        process(verbose=verbose)
        results = vman.finish("Bigger process")
        return results

    return _bigger_process


@parametrize("func", [process, bigger_process])
def test_counter(func):
    results = func(0)

    process_dict = {'subprocesses': 0,
                    'steps': 2}
    bigger_dict = {'subprocesses': 1,
                   'steps': 3}

    exp_results_dict = {'_process': process_dict,
                        '_bigger_process': bigger_dict}

    assert results == exp_results_dict[func.__name__]
