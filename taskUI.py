# the main program to choose which job to do and when

from easygui import *
import sqlite3
import helper
import pandas as pd
import subprocess as sp
import jobs

title = "Task Automation System"

conn = sqlite3.connect('jobs.db')
c = conn.cursor()
helper.newTable(c)


def main():
    msg = "Select a task to perform."
    choices = ["Begin Forwarding Email", "Begin Forwarding Email (and not deliver to original user)",
               "Stop Forwarding Email"]

    choice = choicebox(msg, title, choices)
    runDate = getRunDate()
    runTime = getRunTime()

    if choice == choices[0] or choice == choices[1]:  # Begin Forwarding Email
        msg = "Enter the information."
        fieldNames = ["First name", "Last name", "Username to forward to"]
        FieldValues = multenterbox(msg, title, fieldNames)

        if choice == choices[0]:
            helper.newJob(c, runDate, runTime, "beginEmailForwarding", FieldValues)
        else:
            helper.newJob(c, runDate, runTime, "beginEmailForwardingONLY", FieldValues)

    if choice == choices[2]:  # End Forwarding Email
        msg = "Enter the information."
        fieldNames = ["First name", "Last name"]
        FieldValues = multenterbox(msg, title, fieldNames)

        helper.newJob(c, runDate, runTime, "endEmailForwarding", FieldValues)

    conn.commit()
    sp.call('cls', shell=True)
    print("\nSCHEDULED JOBS\n--------------------------------------------")
    print(pd.read_sql_query("SELECT * FROM jobs", conn))
    conn.close()


def getRunDate():
    msg = "Enter the run date. (DD/MM/YY)"
    startDate = enterbox(msg, title)
    return startDate


def getRunTime():
    extensions = [":00", ":15", ":30", ":45"]
    choices = []
    for i in range(24):
        for j in range(4):
            choices.append(str(i) + extensions[j])
    msg = "Choose a run time."
    choice = choicebox(msg, title, choices)
    return choice


if __name__ == "__main__":
    main()