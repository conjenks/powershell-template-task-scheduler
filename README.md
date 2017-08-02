# ---UNFINISHED---
# Python/PowerShell Task Scheduler

The purpose of this code is to provide users with a task scheduling suite that can be modified and appended to with a user's own customized tasks (likely in the form of Python functions combined with PowerShell scripts).

As of right now, its main focus is as a framework for network administrators or others with similar roles to be able to launch custom PowerShell scripts from templates with variable input at specific run dates/times.

For example, there is currently a PowerShell template script in the `/scripts` directory named `beginEmailForwarding.ps1`. This template takes a First Name, Last Name, and Username as input and launches an Exchange PowerShell script to begin forwarding the email of the {First Name} {Last Name} user to the email address of the {Username} input. Users of this Python Task Scheduler can go into a GUI, select the "Begin Email Forwarding" option, enter the input arguments as well as a run date and time, and the custom script will be launched accordingly. 

# FILE BREAKDOWN

# scheduler.py

The main program which will be run as a Windows service through NSSM. This should not be altered except by project contributors.

# taskUI.py

Implements the `easygui` Python library and, when launched, is the interface for adding the custom jobs to the task scheduler. The user will alter this file, as well as the `jobs.py` file, when adding their own custom tasks.

# jobs.db

The SQLite database that will hold all of the currently scheduled jobs and their necessary attributes. `helper.py` simply contains helper functions for this database, and `printDB.py` prints the database when run.