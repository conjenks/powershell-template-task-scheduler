# to be run as a service, and execute the jobs in jobs.db at their specified run times
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import sqlite3
import helper
import jobs
from time import time

job_dict = {"beginEmailForwarding": jobs.begin_email_forwarding, "beginEmailForwardingONLY": jobs.begin_email_forwarding_only, "endEmailForwarding": jobs.end_email_forwarding}


def main():
    conn = sqlite3.connect('jobs.db')
    write_logs("program started\n")

    scheduler = BackgroundScheduler()
    scheduler.start()

    start = time()
    while True:
        if (time() - start) > 10:
            refresh(conn, scheduler)
            start = time()
        continue


def refresh(conn, scheduler):
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    for row in c:
        if row[4] == 0:  # if job is not scheduled
            write_logs(get_job_description(row))
            schedule(row, scheduler)
            helper.set_job_scheduled(c, row[0])
            conn.commit()


def schedule(row, scheduler):
    job = job_dict[row[3]]
    date_time = get_datetime_from_row(row)
    args = get_args(row)
    # scheduler.add_job(job_function, run_date=date_time) this is the real function

    run_date = datetime.datetime.now()
    run_date = run_date + datetime.timedelta(seconds=10)
    run_date_plus_five = run_date + datetime.timedelta(seconds=5)
    scheduler.add_job(job, run_date=run_date, args=args)  # testing - always do jobs 10 seconds in the future

    scheduler.add_job(helper.remove_job_from_table, run_date=run_date_plus_five, args=[row[0]])


def get_datetime_from_row(row):
    date_time = datetime.datetime.strptime(row[1], "%x")
    date_time = date_time.replace(hour=int(row[2].split(':')[0]), minute=int(row[2].split(':')[1]))
    return date_time


def get_args(row): # extract the arguments from a row and return them in an array
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


def get_job_description(row):
    description = "JOB ADDED - " + str(datetime.datetime.now()) + "\n" \
                  + "Execute at: " + str(get_datetime_from_row(row)) + "\n" \
                  + "Job: " + str(job_dict[row[3]]) + "\n"\
                  + "Arguments: " + str(get_args(row))

    return description


if __name__ == "__main__":
    main()

