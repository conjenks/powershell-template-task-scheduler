# ---UNFINISHED---
# Python/PowerShell Task Scheduler

The purpose of this code is to provide users with a task scheduling suite that can be modified and appended to with a user's own customized tasks (likely in the form of Python functions combined with PowerShell scripts).

As of right now, its main focus is as a framework for network administrators or others with similar roles to be able to launch custom PowerShell scripts from templates with variable input at specific run dates/times.

For example, there is currently a PowerShell template script in the `/scripts` directory named `emailForwarding.ps1`. This template takes a First Name, Last Name, and Username as input and launches an Exchange PowerShell script to begin forwarding the email of the {First Name} {Last Name} user to the email address of the {Username} input. Users of this Python Task Scheduler can go into a GUI, select the "Begin Email Forwarding" option, enter the input arguments as well as a run date and time, and the custom script will be launched accordingly. 

# QUICK USAGE GUIDE

1. Edit the scripts in the `scripts\` directory to apply to your respective Exchange server(s), etc.
2. Set the path in `launch_scheduler.bat` as the absolute path to `scheduler.py` on your system.
3. Install `launch_scheduler.bat` as a Windows service using NSSM[link].
	Make sure the account you install the service with has Python 3 installed as well as the following dependencies (using pip):
		mako
		pandas
		apscheduler
		easygui
4. Start the service, and run `task_ui.py` to begin adding custom tasks to the scheduler!

# FILE BREAKDOWN

# scheduler.py

The main program which will be run as a Windows service through NSSM. This should not be altered except by project contributors.

# taskUI.py

Implements the `easygui` Python library and, when launched, is the interface for adding the custom jobs to the task scheduler. The user will alter this file, as well as the `jobs.py` file, when adding their own custom tasks.

# jobs.db

The SQLite database that will hold all of the currently scheduled jobs and their necessary attributes. `helper.py` simply contains helper functions for this database, and `printDB.py` prints the database when run.

# miscellaneous

`logs.txt` is the log file for the scheduler and `launch_scheduler.bat` is the batch file that is used to run `scheduler.py` as a Windows service.