# defines specific functions for each type of job the automation system can carry out

from mako.template import Template
import subprocess
import sys
import os
import sqlite3

currentPath = os.getcwd()

def beginEmailForwarding(first, last, username):
    template = Template(filename='scripts/emailForwarding.ps1',
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


def beginEmailForwardingONLY(first, last, username):
    template = Template(filename='scripts/emailForwardingONLY.ps1',
                        output_encoding='utf-16',
                        input_encoding='utf-16',
                        encoding_errors='replace')

    filename = first + last + "ForwardingONLY.ps1"
    file = open(filename, 'wb')
    file.write((template.render(FIRST=first, LAST=last, USERNAME=username)))
    file.close()

    p = subprocess.Popen(["powershell.exe", currentPath + "\\" + filename], stdout=sys.stdout)

    while True:
        if p.poll() is not None:  # if the subprocess is done running
            os.remove(filename)
            break


def endEmailForwarding(first, last):
    template = Template(filename='scripts/removeEmailForwarding.ps1',
                        output_encoding='utf-16',
                        input_encoding='utf-16',
                        encoding_errors='replace')

    filename = first + last + "StopForwarding.ps1"
    file = open(filename, 'wb')
    file.write((template.render(FIRST=first, LAST=last)))
    file.close()

    # NEEDS EVAULATED
    with open('logs.txt', 'a') as logs:
        logs.write("\n")
        p = subprocess.Popen(["powershell.exe", currentPath + "\\" + filename], stdout=logs)
    logs.close()
    

    while True:
        if p.poll() is not None:
            os.remove(filename)
            break

def removeJobFromTable(id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    c.execute("DELETE FROM jobs WHEREo ID=?", (id,))
    conn.commit()
