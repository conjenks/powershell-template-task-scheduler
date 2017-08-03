# the GUI program to choose which job to do and when

from easygui import *
import sqlite3
import helper
import pandas as pd
import subprocess as sp

title = "Task Automation System"

conn = sqlite3.connect('jobs.db')
c = conn.cursor()
helper.new_table(c)


def main():
    msg = "Select a task to perform."
    choices = ["Begin Forwarding Email", "Begin Forwarding Email (and not deliver to original user)",
               "Stop Forwarding Email"]

    choice = choicebox(msg, title, choices)
    run_date = get_run_date()
    run_time = get_run_time()

    if choice == choices[0] or choice == choices[1]:  # Begin Forwarding Email
        msg = "Enter the information."
        field_names = ["First name", "Last name", "Username to forward to"]
        field_values = multenterbox(msg, title, field_names)

        if choice == choices[0]:
            helper.new_job(c, run_date, run_time, "begin_email_forwarding", field_values)
        else:
            helper.new_job(c, run_date, run_time, "begin_email_forwarding_only", field_values)

    if choice == choices[2]:  # End Forwarding Email
        msg = "Enter the information."
        field_names = ["First name", "Last name"]
        field_values = multenterbox(msg, title, field_names)

        helper.new_job(c, run_date, run_time, "end_email_forwarding", field_values)

    conn.commit()
    sp.call('cls', shell=True)
    print("\nSCHEDULED JOBS\n--------------------------------------------")
    print(pd.read_sql_query("SELECT * FROM jobs", conn))
    conn.close()


def get_run_date():
    msg = "Enter the run date. (DD/MM/YY)"
    start_date = enterbox(msg, title)
    return start_date


def get_run_time():
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