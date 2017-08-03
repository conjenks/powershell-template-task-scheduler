# defines the functions to interact with jobs.db
import sqlite3


def new_job(cursor, date, time, job, args):
    sql = "INSERT INTO jobs VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (date, time, job, False)
    for i in range(6):
        if i < len(args):
            values = values + (args[i], )
        else:
            values = values + (None, )
    cursor.execute(sql, values)


def new_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs 
            (id integer primary key autoincrement, date text, time text, job text, scheduled boolean, 
            arg1 text, arg2 text, arg3 text, arg4 text, arg5 text, arg6 text)''')


def set_job_scheduled(cursor, rowid):
    cursor.execute("UPDATE jobs SET scheduled=1 WHERE ID=?", (rowid,))


def remove_job_from_table(id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    c.execute("DELETE FROM jobs WHERE ID=?", (id,))
    conn.commit()