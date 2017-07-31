# defines the functions to interact with jobs.db
import sqlite3


def newJob(cursor, date, time, job, args):
    sql = "INSERT INTO jobs VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (date, time, job, False)
    for i in range(6):
        if i < len(args):
            values = values + (args[i], )
        else:
            values = values + (None, )
    cursor.execute(sql, values)


def newTable(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs 
            (id integer primary key autoincrement, date text, time text, job text, scheduled boolean, 
            arg1 text, arg2 text, arg3 text, arg4 text, arg5 text, arg6 text)''')


def setJobScheduled(cursor, rowid):
    cursor.execute("UPDATE jobs SET scheduled=1 WHERE ID=?", (rowid,))
