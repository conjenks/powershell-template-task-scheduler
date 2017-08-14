# defines specific functions for each type of job the automation system can carry out

from mako.template import Template
import subprocess
import os
import sqlite3

currentPath = os.getcwd()


def begin_email_forwarding(first, last, username):
    template = get_template("email_forwarding.ps1")

    filename = first + last + "Forwarding.ps1"
    file = open(filename, 'wb')
    file.write((template.render(FIRST=first, LAST=last, USERNAME=username)))
    file.close()

    run_script_and_log(filename)


def end_email_forwarding(first, last):
    template = get_template("end_email_forwarding.ps1")

    filename = first + last + "StopForwarding.ps1"
    file = open(filename, 'wb')
    file.write((template.render(FIRST=first, LAST=last)))
    file.close()

    run_script_and_log(filename)


def get_template(script_name):
    script = 'scripts/' + script_name
    template = Template(filename=script,
                        output_encoding='utf-16',
                        input_encoding='utf-16',
                        encoding_errors='replace')
    return template


def run_script_and_log(filename):
    with open('logs.txt', 'a') as logs:
        logs.write("\n____________________________________________________________\n\n")
        logs.write(" ** FUNCTION OUTPUT\n\n")
        p = subprocess.Popen(["powershell.exe", currentPath + "\\" + filename], stdout=logs)
    logs.close()

    while True:
        if p.poll() is not None:
            os.remove(filename)
            break


def remove_job_from_table(job_id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    c.execute("DELETE FROM jobs WHERE ID=?", (job_id,))
    conn.commit()
