---
layout: default
---

about
=====

This section is a Q&A on various verbosemanager-related topics.

*Q. What is verbosemanager?*  
A. verbosemanager is a module revolving around the VerboseManager class, which provides tools for managing complex processes.

*Q. What do you mean by 'complex process'?*  
A. By 'complex process' I mean one that takes a particularly long time or consists of multiple smaller sub-processes; essentially, any algorithm that does enough that you'd like to know what's going on as it runs, or assess the individual parts of it from the user side.

*Q. Why should I use this instead of another progress bar module?*  
A. Existing modules, like [tqdm](https://tqdm.github.io/) or [progressbar2](https://pypi.org/project/progressbar2/) are amazing (I think tqdm's efficient iterable wrapping is genius) but I felt like they'd both taken the niche of progress bars for iterables. This module is instead designed for long, user-facing algorithms, such as those in scientific software.

