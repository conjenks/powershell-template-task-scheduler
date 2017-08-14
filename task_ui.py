# the GUI program to choose which job to do and when

from easygui import *
from helper import *
import pandas as pd
import subprocess as sp

title = "Python Task Scheduler"

conn = sqlite3.connect('jobs.db')
c = conn.cursor()
new_table(c)
task_list = list(job_dict.keys())


def main():

    choice = select_task()

    run_date = get_run_date()
    run_time = get_run_time()

    msg = "Enter the information."

    if choice == task_list[0]:  # Begin Forwarding Email

        field_names = ["First name", "Last name", "Username to forward to"]
        field_values = multenterbox(msg, title, field_names)

        new_job(c, run_date, run_time, "begin_email_forwarding", field_values)

    if choice == task_list[1]:  # End Forwarding Email

        field_names = ["First name", "Last name"]
        field_values = multenterbox(msg, title, field_names)

        new_job(c, run_date, run_time, "end_email_forwarding", field_values)

    conn.commit()
    sp.call('cls', shell=True)
    print("\nSCHEDULED JOBS\n--------------------------------------------")
    print(pd.read_sql_query("SELECT * FROM jobs", conn))
    conn.close()


def select_task():
    msg = "Select a task to perform."
    choice = choicebox(msg, title, task_list)
    return choice


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