"""Expected stdouts for each fixture of test_verbose_manager.py at each verbosity level."""

# stdout for the fixtures at each verbosity level
EXP_STDOUT = {
    "process_stdout": {
        1: "Process complete in 0.03 seconds.",
        2: (
            "Process complete in 0.03 seconds.\n"
            "Timings per step:\n"
            "Initialising: 0.01\n"
            "Process step 1: 0.01\n"
            "Process step 2: 0.01\n"
        ),
        3: (
            "\n"
            "\r"
            "\r"
            "[                    ] 0%  Initialising\r"
            "                                       \r"
            "[==========          ] 50%  Process step 1; previous step took 0.01 "
            "seconds.\r"
            "                                                                            \r"
            "[====================] 100%  Process step 2; previous step took 0.01 "
            "seconds.\n"
            "Process complete in 0.03 seconds.\n"
            "Timings per step:\n"
            "Initialising: 0.01\n"
            "Process step 1: 0.01\n"
            "Process step 2: 0.01\n"
        ),
    },
    "bigger_process_stdout": {
        1: "Bigger process complete in 0.05 seconds.\n",
        2: "Bigger process complete in 0.05 seconds.\n"
        "Timings per step:\n"
        "Initialising: 0.01\n"
        "Bigger process step 1: 0.02\n"
        "Subprocess: \n"
        "|Process step 1: 0.01\n"
        "|Process step 2: 0.01\n",
        3: (
            "\n"
            "\r"
            "\r"
            "[                    ] 0%  Initialising\r"
            "                                       \r"
            "[======              ] 33%  Bigger process step 1; previous step took 0.01 "
            "seconds.\r"
            "                                                                                   \r"
            "[=============       ] 66%  Process step 1; previous step took 0.02 "
            "seconds.\r"
            "                                                                            \r"
            "[====================] 100%  Process step 2; previous step took 0.01 "
            "seconds.\n"
            "Bigger process complete in 0.05 seconds.\n"
            "Timings per step:\n"
            "Initialising: 0.01\n"
            "Bigger process step 1: 0.02\n"
            "Subprocess: \n"
            "|Process step 1: 0.01\n"
            "|Process step 2: 0.01\n"
        ),
    },
    "iterative_process_stdout": {
        1: "Iterative process complete in 0.31 seconds.\n",
        2: "Iterative process complete in 0.31 seconds.\n"
        "Timings per step:\n"
        "Initialising: 0.01\n"
        "Entering iterator: \n"
        "|Iterator step 1: Average 0.03 over 5 iterations\n"
        "|Iterator step 2: Average 0.03 over 5 iterations\n"
        "Iterator: 0.3\n"
        "Finishing: 0.0\n",
        3: (
            "\n"
            "\r"
            "\r"
            "[                    ] 0%  Initialising\r"
            "                                       \r"
            "[==========          ] 50%  Iterator; previous step took 0.01 seconds.\r"
            "                                                                      \r"
            "[==========          ] 50%  Iterator step 1\r"
            "                                           \r"
            "[==========          ] 50%  Iterator step 2 for iteration 0\r"
            "                                                           \r"
            "[==========          ] 50%  Iterator step 1\r"
            "                                           \r"
            "[==========          ] 50%  Iterator step 2 for iteration 1\r"
            "                                                           \r"
            "[==========          ] 50%  Iterator step 1\r"
            "                                           \r"
            "[==========          ] 50%  Iterator step 2 for iteration 2\r"
            "                                                           \r"
            "[==========          ] 50%  Iterator step 1\r"
            "                                           \r"
            "[==========          ] 50%  Iterator step 2 for iteration 3\r"
            "                                                           \r"
            "[==========          ] 50%  Iterator step 1\r"
            "                                           \r"
            "[==========          ] 50%  Iterator step 2 for iteration 4\r"
            "                                                           \r"
            "[====================] 100%  Finishing; previous step took 0.3 seconds.\n"
            "Iterative process complete in 0.31 seconds.\n"
            "Timings per step:\n"
            "Initialising: 0.01\n"
            "Entering iterator: \n"
            "|Iterator step 1: Average 0.03 over 5 iterations\n"
            "|Iterator step 2: Average 0.03 over 5 iterations\n"
            "Iterator: 0.3\n"
            "Finishing: 0.0\n"
        ),
    },
}
