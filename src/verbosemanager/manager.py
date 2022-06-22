"""Module for the regular verbose manager class and the manager mixin class"""
import sys
import warnings
from statistics import mean
from time import time, asctime, localtime
from typing import Union, Optional

from .counter import Counter

# pylint: disable=attribute-defined-outside-init, disallowed-name


class VerboseManager:
    """VerboseManager is a Singleton pattern class which manages verbose printing of a process."""

    _instance: Union["VerboseManager", Counter, None] = None
    # max_print_len decides how many lines of output are printed to stdout
    # before they are printed to file instead; this can be changed by user
    max_output_len = 20

    def __init__(self):
        raise RuntimeError(
            "VerboseManager should not be instantiated directly. Use VerboseManager.instance()."
        )

    @classmethod
    def instance(cls, counter=False):
        """
        Instantiates a VerboseManager if one does not exist,
        and returns the existing one if it does exist.

        Parameters:
        -----------
        counter: bool = False
            If True, replaces the manager with a Counter object,
            which returns info on your process' verbose output.
            Used for development.
        """
        if counter:
            return Counter.instance()
        # if a subprocess doesn't have counter=True, don't create a manager on top of the counter
        if isinstance(cls._instance, Counter):
            return cls._instance
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        """
        Sets variables to how they should be set when VerboseManager is instantiated
        """
        self.times = False
        self.bar = False
        self.start_time = time()
        self.step_times = False
        self.step_time = time()
        self._in_progress = False
        self.subprocesses = 0
        self.timings_list = []
        self.subprocess_start_times = []
        self.buffer = None
        self.prev_message = "Initialising"
        self.eraser_len = 0
        self.progress = 0
        self.maximum = 0
        self.iter_steps = {}
        self.iterating = False

    def start(self, n_steps: int, verbose: int = 0):
        """
        Initialises progress management, including times and a progress bar.
        If a progress bar is already running, accounts for the subprocess which called this.

        Parameters
        ----------
        n_steps: int
            The amount of steps involved in the process (including those in subprocesses).
        verbose: int
            The level of verbosity:
            Verbose level 0 gives no information.
            Verbose level 1 gives final time for a whole process.
            Verbose level 2 gives final time and also a progress bar.
            Verbose level 3 gives final time, a progress bar, and time per step.
        """
        # activate features based on verbosity level
        if verbose >= 1:
            self.times = True
        if verbose >= 2:
            self.step_times = True
        if verbose >= 3:
            self.bar = True

        if not self._in_progress:
            # if not in progress, initialise process
            self._in_progress = True
            self.progress = 0
            self.maximum = n_steps

            if self.times:
                self.start_time = time()
            if self.bar:
                sys.stdout.write("\n")
                self._print_progress(0, self.maximum, "Initialising")
            if self.step_times:
                self.step_time = self.start_time
        else:
            # else, a subprocess called this method; account for it
            self.subprocesses += 1
            self.subprocess_start_times.append(time())

    def step(self, message: str):
        """
        Increases progress by one 'step' towards maximum, updating progress bar if necessary.

        Parameters
        ----------
        message: str
            a message which says what the current step is doing.
        """
        self.progress += 1

        # if verbosity is >=2, give step time with bar message and record it for final result
        if self.step_times:
            message_time = time() - self.step_time
            # append previous step to timings list
            self.timings_list.append((self.prev_message, round(message_time, 2)))
            # if a header is buffered, add it now so it's in the right place
            if self.buffer is not None:
                self.timings_list.append(self.buffer)
                self.buffer = None
            # add vertical bars to denote nesting level in final list
            # and add previous timing to progress bar message
            self.prev_message = f"{'|' * self.subprocesses}{message}"
            message += f"; previous step took {round(message_time, 2)} seconds."
            self.step_time = time()

        # if verbosity is 3, print progress bar
        if self.bar:
            self._print_progress(self.progress, self.maximum, message)

    def header(self, message: str):
        """
        Adds a line to final step timings print without affecting step progress or advancement.

        Parameters
        ----------
        message: str
            The header message that will be printed.
        """

        # since a step isn't added to the timings list until it is finished,
        # this will print one step too early unless we buffer it and add
        # it after the current step completes
        self.buffer = ("|" * self.subprocesses + message, "")

    def finish(self, process_name: str) -> Union[None, float, list]:
        """
        Prints final times for the process.

        Parameters
        ----------
        process_name: str
            a message which gives the name of the process being managed.

        Returns
        -------
        float
            the runtime in seconds for the process or subprocess that just finished.
        """
        # fallback to timings as None if there's no timings to return
        timings = None

        # if all processes are finished, finalise verbose printing
        if self._in_progress and self.subprocesses == 0:
            # give warning to developer if self.maximum is set incorrectly
            if self.progress != self.maximum:
                warnings.warn(
                    f'verbose steps for process "{process_name}" is set incorrectly: '
                    f"it is equal to {self.maximum}, "
                    f"but the process took {self.progress} steps.",
                    stacklevel=2,
                )

            # print final results
            if self.times:
                timings = time()
                # the newline spaces are nice if the bar is there, but too spacious without it.
                if self.bar:
                    sys.stdout.write("\n")
                print(
                    f"{process_name} complete in {round(timings - self.start_time, 2)} seconds."
                )
                if self.step_times:
                    # append final step to timings list and then print timings per step
                    self.timings_list.append(
                        (self.prev_message, round(time() - self.step_time, 2))
                    )
                    self._print_step_timings(process_name)

                    # save timings list for return after we reset it
                    timings = self.timings_list

            # reset parameters to how they were when VerboseManager was initialised
            self.init()

        elif self._in_progress:
            # else, a subprocess called this method; account for it
            # but also return whole subprocess timing
            self.subprocesses -= 1
            timings = time() - self.subprocess_start_times[-1]
            self.subprocess_start_times.pop()

        else:
            warnings.warn(
                "VerboseManager.finish() was called, but no management process was running."
            )

        return timings

    def iterate(self, message: str, iteration_message: Optional[str] = None):
        """Saves information on a step inside an iterator

        Parameters
        ----------
        message: str
            The overall message for this step. Used in final timings list.
        iteration_message: str, optional
            An optional message for this specific iteration, used in the progress bar.
        """
        if self.iterating is False:
            self.iterating = True
            self.prev_iter_step_time = time()
            self.header("Entering iterator")
            self.step("Iterator")

        if self.step_times:
            try:
                self.iter_steps[message].append(time() - self.prev_iter_step_time)
            except KeyError:  # if this iter step hasn't been run yet
                self.iter_steps[message] = []

            if self.bar:
                if iteration_message:
                    iteration_message = " " + iteration_message
                else:
                    iteration_message = ""
                self._print_progress(
                    self.progress, self.maximum, f"{message}{iteration_message}"
                )

            self.prev_iter_step_time = time()

    def finish_iterate(self):
        """Finishes an iterator and adds iterator steps to the step list"""
        if self.step_times:
            if len(self.iter_steps) == 0:
                raise RuntimeError(
                    "finish_iterate() was run, but no iterator steps exist."
                )

            for key, times in self.iter_steps.items():
                iterations = len(times)
                self.iter_steps[key] = mean(times)
                self.timings_list.append(
                    (
                        f"{'|' * (self.subprocesses + 1)}{key}",
                        f"Average {round(self.iter_steps[key], 2)} "
                        f"over {iterations + 1} iterations",
                    )
                )

            self.iter_steps = {}
            self.iterating = False

    def _print_progress(self, i, maximum, message):
        """
        Prints out a progress bar, which looks like (e.g.)
        [================    ] 80%  message
        """
        bar_size = 20
        try:
            progress = i / maximum
        except ZeroDivisionError:
            warnings.warn("Your function has zero verbose steps. Was this intentional?")
            return

        eraser = f'{" " * self.eraser_len}'

        # we use sys.stdout.write() instead of print()
        # because print() creates a new line at the end;
        # we don't want this, we want to stay on the same line,
        #  so we can use \r to overwrite the bar.
        # \r is 'carriage return' - it returns to the start of line for overwriting.
        sys.stdout.write(f"\r{eraser}\r")
        sys.stdout.write(
            f"[{'=' * int(bar_size * progress):{bar_size}s}] "
            f"{int(100 * progress)}%  {message}"
        )
        # get length of eraser for next message
        self.eraser_len = len(
            f"[{'=' * int(bar_size * progress):{bar_size}s}] "
            f"{int(100 * progress)}%  {message}"
        )

    @classmethod
    def _print_step_timings(cls, process_name):
        """
        Prints final step timings, either to stdout (if below max_print_len)
        or to file (if above max_print_len)

        This is a class method as we need to access cls.max_print_len.
        """

        if len(cls._instance.timings_list) > cls.max_output_len:
            print(
                "Timings list is too long, so has been printed to the file timings.log."
                " To change how many steps are recorded until we print to file instead"
                " of output, set max output length with"
                " VerboseManager.max_output_len = [your desired length]"
            )
            with open("timings.log", "a", encoding="utf-8") as logfile:
                # prints title line in case multiple timings are printed to same log
                logfile.write(
                    f"\nTimings for {process_name.lower()} on {asctime(localtime(time()))}\n"
                )
                for step_timing in cls._instance.timings_list:
                    logfile.write(f"{step_timing[0]}: {step_timing[1]}\n")
        else:
            print("Timings per step:")
            for step_timing in cls._instance.timings_list:
                print(f"{step_timing[0]}: {step_timing[1]}")
