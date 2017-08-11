# defines specific functions for each type of job the automation system can carry out

from mako.template import Template
import subprocess
import sys
import os
import sqlite3

currentPath = os.getcwd()


def begin_email_forwarding(first, last, username):
    template = Template(filename='scripts/email_forwarding.ps1',
                        output_encoding='utf-16',
                        input_encoding='utf-16',
                        encoding_errors='replace')

    filename = first + last + "Forwarding.ps1"
    file = open(filename, 'wb')
    file.write((template.render(FIRST=first, LAST=last, USERNAME=username)))
    file.close()

    p = subprocess.Popen(["powershell.exe", currentPath + "\\" + filename], stdout=sys.stdout)

    while True:
        if p.poll() is not None:  # if the subprocess is done running
            os.remove(filename)
            break


def begin_email_forwarding_only(first, last, username):
    template = Template(filename='scripts/email_forwarding_only.ps1',
                        output_encoding='utf-16',
                        input_encoding='utf-16',
                        encoding_errors='replace')

    filename = first + last + "ForwardingONLY.ps1"
    file = open(filename, 'wb')
    file.write((template.render(FIRST=first, LAST=last, USERNAME=username)))
    file.close()

    # NEEDS EVALUATED
    with open('logs.txt', 'a') as logs:
        logs.write("\n____________________________________________________________\n\n")
        logs.write(" ** FUNCTION OUTPUT -- needs identification method\n\n")
        p = subprocess.Popen(["powershell.exe", currentPath + "\\" + filename], stdout=logs)
    logs.close()

    while True:
        if p.poll() is not None:  # if the subprocess is done running
            os.remove(filename)
            break


def end_email_forwarding(first, last):
    template = Template(filename='scripts/end_email_forwarding.ps1',
                        output_encoding='utf-16',
                        input_encoding='utf-16',
                        encoding_errors='replace')

    filename = first + last + "StopForwarding.ps1"
    file = open(filename, 'wb')
    file.write((template.render(FIRST=first, LAST=last)))
    file.close()

    # NEEDS EVALUATED
    with open('logs.txt', 'a') as logs:
        logs.write("\n____________________________________________________________\n\n")
        logs.write(" ** FUNCTION OUTPUT -- needs identification method\n\n")
        p = subprocess.Popen(["powershell.exe", currentPath + "\\" + filename], stdout=logs)
    logs.close()

    while True:
        if p.poll() is not None:
            os.remove(filename)
            break


def remove_job_from_table(id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    c.execute("DELETE FROM jobs WHERE ID=?", (id,))
    conn.commit()
