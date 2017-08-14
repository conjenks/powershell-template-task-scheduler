# defines the functions to interact with jobs.db
import sqlite3
import jobs
import datetime

job_dict = {"begin_email_forwarding": jobs.begin_email_forwarding,
            "begin_email_forwarding_only": jobs.begin_email_forwarding_only,
            "end_email_forwarding": jobs.end_email_forwarding}


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
            (id integer primary key autoincrement, 
            date text, 
            time text, 
            job text, 
            scheduled boolean, 
            arg1 text, 
            arg2 text, 
            arg3 text, 
            arg4 text, 
            arg5 text, 
            arg6 text)''')


def set_job_scheduled(cursor, rowid):
    cursor.execute("UPDATE jobs SET scheduled=1 WHERE ID=?", (rowid,))


def remove_job_from_table(id):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    c.execute("DELETE FROM jobs WHERE ID=?", (id,))
    conn.commit()


def get_job_description(row):
    description = "JOB ADDED ON - " + str(datetime.datetime.now()) + "\n" \
                  + "Execute at: " + str(get_datetime_from_row(row)) + "\n" \
                  + "Job: " + str(job_dict[row[3]]) + "\n"\
                  + "Arguments: " + str(get_args(row))

    return description


def get_datetime_from_row(row):
    date_time = datetime.datetime.strptime(row[1], "%x")
    date_time = date_time.replace(hour=int(row[2].split(':')[0]), minute=int(row[2].split(':')[1]))
    return date_time


def get_args(row):  # extract the arguments from a row and return them in an array
    args = []
    i = 5
    while row[i] is not None:
        args.append(row[i])
        i += 1
    return args


def write_logs(string):
    with open('logs.txt', 'a') as f:
        f.write("\n____________________________________________________________\n\n")
        f.write(string)
    f.close()