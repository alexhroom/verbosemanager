import pytest
from pytest_cases import parametrize
from time import sleep

from src import verbosemanager


@pytest.fixture
def process(**verbose):
    """A mock process for testing."""

    def _process(**verbose):
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
        sleep(0.01)
        verbose_manager.step("Bigger process step 1")
        sleep(0.01)
        verbose_manager.header("Subprocess")
        process(verbose=verbose)

    return _bigger_process


@parametrize("verbose", [1, 2, 3])
@parametrize('process, n_steps', [(process, 2), (bigger_process, 3)])
def test_decorator(verbose, process, n_steps):
    """Tests the verbosemanager decorator"""

    @verbosemanager(n_steps=n_steps)
    def func(fn, **verbose):
        fn(verbose=verbose)

    func(process, verbose=verbose)
